#!/usr/bin/env python3
"""
PyTune Pro - Herramienta para descarga de audio
Versión optimizada con gestión mejorada de entrada/salida
"""

import yt_dlp
import os
import sys
import argparse
import re
import subprocess
from pathlib import Path
from datetime import datetime

# Configuración global
VERSION = "1.3.0"
MAX_RETRIES = 3
DEFAULT_OUTPUT = Path.home() / "Música" / "PyTune"
SUPPORTED_DOMAINS = [
    'youtube.com', 'youtu.be', 'soundcloud.com', 'bandcamp.com',
    'vimeo.com', 'dailymotion.com', 'tiktok.com'
]

def verificar_dependencias():
    """Verifica que FFmpeg esté instalado"""
    try:
        subprocess.run(['ffmpeg', '-version'], 
                       stdout=subprocess.DEVNULL, 
                       stderr=subprocess.DEVNULL,
                       check=True)
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        print("\nERROR: FFmpeg no está instalado o no se encuentra en el PATH")
        print("Es necesario para la conversión de audio")
        print("Instalación:")
        print("  Linux:   sudo apt install ffmpeg")
        print("  macOS:   brew install ffmpeg")
        print("  Windows: Descargar desde https://ffmpeg.org/download.html")
        return False

def validar_url(url):
    """Valida que la URL sea de un dominio soportado"""
    if not re.match(r'^https?://', url):
        return False
        
    dominio = re.search(r'://([^/]+)', url)
    if not dominio:
        return False
        
    dominio = dominio.group(1).lower()
    return any(supported in dominio for supported in SUPPORTED_DOMAINS)

def crear_directorio_salida(ruta):
    """Crea el directorio de salida con manejo de errores"""
    try:
        ruta.mkdir(parents=True, exist_ok=True)
        return True
    except PermissionError:
        print(f"\nERROR: Sin permisos para crear directorio: {ruta}")
    except OSError as e:
        print(f"\nERROR: No se pudo crear directorio: {e}")
    return False

def progreso_hook(d):
    """Muestra el progreso de la descarga"""
    if d['status'] == 'downloading':
        porcentaje = d.get('percent')
        velocidad = d.get('speed')
        eta = d.get('eta')
        
        if porcentaje:
            bar_length = 40
            completado = int(bar_length * porcentaje / 100)
            barra = f"[{'=' * completado}{' ' * (bar_length - completado)}]"
            
            sys.stdout.write(
                f"\r{barra} {porcentaje:5.1f}% | "
                f"ETA: {eta}s | "
                f"Vel: {velocidad/1024/1024 if velocidad else 0:.1f}MB/s"
            )
            sys.stdout.flush()
    
    elif d['status'] == 'finished':
        sys.stdout.write("\n✓ Descarga completada, convirtiendo...\n")

def descargar_audio(url, output_path):
    """
    Descarga y convierte audio a MP3 con manejo profesional de errores
    """
    # Configuración de yt-dlp
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': str(output_path / '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
        'writethumbnail': True,
        'embedthumbnail': True,
        'writedescription': False,
        'writeinfojson': False,
        'writesubtitles': False,
        'writeautomaticsub': False,
        'ignoreerrors': False,
        'quiet': False,
        'no_warnings': False,
        'progress_hooks': [progreso_hook],
        'postprocessor_args': [
            '-metadata', 'comment=Descargado con PyTune',
            '-metadata', f'encoder=PyTune v{VERSION}'
        ],
        'retries': 10,
        'fragment_retries': 10,
        'skip_unavailable_fragments': True,
        'keepvideo': False,
        'concurrent_fragment_downloads': 5,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            
            # Para playlists
            if 'entries' in info:
                playlist_title = info.get('title', 'playlist')
                print(f"\nPlaylist descargada: {playlist_title}")
                return True
                
            # Para videos individuales
            filename = ydl.prepare_filename(info)
            mp3_file = Path(filename).with_suffix('.mp3')
            
            if mp3_file.exists():
                print(f"✅ Descarga exitosa: {mp3_file.name}")
                return True
                
            return False

    except yt_dlp.utils.DownloadError as e:
        print(f"\nERROR de descarga: {e}")
        return False

    except Exception as e:
        print(f"\nERROR inesperado: {e}")
        return False

def procesar_entrada_usuario():
    """Maneja la entrada interactiva del usuario de forma robusta"""
    urls = []
    print("\nModo interactivo (escribe 'salir' para terminar)")
    
    while True:
        try:
            entrada = input("\nIngresa URL o 'listo': ").strip()
            
            if not entrada:
                continue
                
            if entrada.lower() in ['exit', 'quit', 'salir','listo','ok']:
                break
                
            if validar_url(entrada):
                urls.append(entrada)
                print(f"URL añadida: {entrada}")
            else:
                print("⚠️ URL inválida o no soportada. Intenta nuevamente.")
                
        except KeyboardInterrupt:
            print("\n⏹️ Entrada cancelada")
            break
        except EOFError:
            print("\n⏹️ Fin de entrada")
            break
        except Exception as e:
            print(f"\n⚠️ Error procesando entrada: {e}")
    
    return urls

def main():
    # Configuración del parser de argumentos
    parser = argparse.ArgumentParser(
        description='Descarga audio de YouTube y otros sitios en formato MP3, MP4, WEPM',
        add_help=False
    )
    
    parser.add_argument(
        'url',
        nargs='?',
        default=None,
        help='URL del contenido a descargar'
    )
    
    parser.add_argument(
        '-o', '--output',
        default=DEFAULT_OUTPUT,
        help=f'Directorio de salida (por defecto: {DEFAULT_OUTPUT})'
    )
    
    parser.add_argument(
        '-b', '--batch',
        help='Archivo con lista de URLs (una por línea)'
    )
    
    parser.add_argument(
        '-v', '--version',
        action='version',
        version=f'PyTune v{VERSION}'
    )
    
    parser.add_argument(
        '-h', '--help',
        action='help',
        default=argparse.SUPPRESS,
        help='Mostrar este mensaje de ayuda'
    )
    
    args = parser.parse_args()
    
    print(f"\nPyTune v{VERSION} - Herramienta profesional de descarga de audio")
    
    # Verificar dependencias
    if not verificar_dependencias():
        sys.exit(1)
    
    # Preparar directorio de salida
    output_path = Path(args.output).resolve()
    if not crear_directorio_salida(output_path):
        sys.exit(1)
    
    # Recolectar URLs
    urls = []
    
    # URL desde argumento
    if args.url:
        if validar_url(args.url):
            urls.append(args.url)
        else:
            print(f"⚠️ URL no soportada: {args.url}")
    
    # URLs desde archivo batch
    if args.batch:
        try:
            with open(args.batch, 'r') as f:
                for line in f:
                    url = line.strip()
                    if url and validar_url(url):
                        urls.append(url)
            print(f"📚 Leídas {len(urls)} URLs desde {args.batch}")
        except Exception as e:
            print(f"❌ Error leyendo archivo batch: {e}")
    
    # Modo interactivo si no hay URLs
    if not urls:
        urls = procesar_entrada_usuario()
    
    if not urls:
        print("\n❌ No se proporcionaron URLs válidas")
        sys.exit(1)
    
    # Procesar descargas
    total = len(urls)
    exitosas = 0
    
    print(f"\n⏬ Iniciando descarga de {total} elemento(s)...\n")
    inicio = datetime.now()
    
    for i, url in enumerate(urls, 1):
        print(f"\n{'='*50}")
        print(f"📥 Descargando elemento {i}/{total}: {url}")
        
        for intento in range(1, MAX_RETRIES + 1):
            if intento > 1:
                print(f"🔄 Reintento {intento}/{MAX_RETRIES}")
                
            if descargar_audio(url, output_path):
                exitosas += 1
                break
            else:
                if intento < MAX_RETRIES:
                    print(f"⏳ Esperando 3 segundos antes de reintentar...")
                    import time
                    time.sleep(3)
    
    # Mostrar resumen
    duracion = datetime.now() - inicio
    print(f"\n{'='*50}")
    print("🏁 Resumen de descargas:")
    print(f"  Total:     {total}")
    print(f"  Exitosas:  {exitosas}")
    print(f"  Fallidas:  {total - exitosas}")
    print(f"  Duración:  {duracion}")
    print(f"  Directorio: {output_path}")
    print(f"{'='*50}\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⛔ Programa interrumpido por el usuario")
        sys.exit(130)
    except Exception as e:
        print(f"\n🔥 Error crítico: {e}")
        sys.exit(1)
