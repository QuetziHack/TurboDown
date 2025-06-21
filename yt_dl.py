import yt_dlp
import os

def descargar_mp3(url, output_path=''):
    # Definir opciones de yt-dlp
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
        'keepvideo': False,  # No guardar el archivo original
    }

    # Descargar el audio usando yt-dlp
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        title = info_dict.get('title', None)
        ext = info_dict.get('ext', None)
        mp3_file = f"{title}.mp3"

    print(f"Archivo MP3 descargado: {mp3_file}")

url = input("Ingresa la url: ")

# Llamar a la función para descargar y convertir
descargar_mp3(url)
