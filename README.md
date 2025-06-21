# yt_dl.py - Descarga de audio con yt-dlp

[![Python Version](https://img.shields.io/badge/python-3.7%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> Script de línea de comandos para descargar audio (música/podcasts, etc.) desde URLs (YouTube y otros soportados por yt-dlp), con opción de conservar la mejor calidad original o convertir a MP3 de alta tasa de bits.

---

## Descripción

`yt_dl.py` es un script en Python que utiliza la biblioteca [yt-dlp](https://github.com/yt-dlp/yt-dlp) para:
- Descargar la mejor pista de audio disponible de una URL (YouTube, Vimeo, SoundCloud, etc.).
- Guardar el archivo en su formato original (por ejemplo, `.m4a`, `.webm`, `.opus`, según el sitio) para conservar la calidad tal como se ofrece.
- Opcionalmente convertir (recodificar) el audio a MP3 con bitrate configurable (por ejemplo, 320 kbps).
- Mostrar una barra de progreso en consola con porcentaje, tamaño, velocidad y ETA.
- Procesar playlists completas o múltiples URLs listadas en un archivo.
- Manejar errores de descarga sin abortar todo el proceso.
- Crear directorios de salida según sea necesario y mostrar rutas de archivos resultantes.

---

## Características principales

- **Mejor calidad disponible por defecto**: se descarga el flujo de audio de mayor calidad que ofrece el servidor.
- **Conservación del formato original**: al no recodificar, se evita pérdida adicional debido a recodificación.
- **Conversión opcional a MP3**: si se requiere compatibilidad con reproductores que no admitan otros formatos, con bitrate alto (configurable).
- **Soporte de playlists**: si se pasa una URL de playlist o un archivo con múltiples URLs, descarga todos los ítems, ignorando errores individuales.
- **Barra de progreso personalizada**: hook que muestra porcentaje, tamaño descargado vs total, ETA y velocidad en la terminal.
- **Manejo de directorio de salida**: crea carpetas si no existen.
- **Lectura de URLs desde archivo**: con prefijo `@archivo.txt`, se procesan varias URLs listadas (una por línea), ignorando líneas vacías o comentarios.
- **Mensajes claros**: informa al usuario sobre archivos resultantes, errores individuales y resumen de descarga de playlists.
- **Configuración vía argumentos de línea de comandos** con `argparse`.

---

## Requisitos

1. **Python 3.7+** (se recomienda 3.9+ o 3.11).  
2. **yt-dlp** instalado en el entorno virtual o global:
   ```bash
   pip install yt-dlp
   ```

3. **ffmpeg** instalado y accesible en el PATH del sistema, para la conversión a MP3 o cualquier procesamiento con postprocesadores de ffmpeg. En sistemas Debian/Ubuntu:

   ```bash
   sudo apt update
   sudo apt install ffmpeg
   ```

   En macOS con Homebrew:

   ```bash
   brew install ffmpeg
   ```

   En Windows, descarga desde [https://ffmpeg.org/](https://ffmpeg.org/) y agrega al PATH.

---

## Instalación

1. Clona o descarga este repositorio:

   ```bash
   git clone https://github.com/tu-usuario/tu-repo-yt-dl.git
   cd tu-repo-yt-dl
   ```
2. Crea un entorno virtual (opcional pero recomendado):

   ```bash
   python3 -m venv venv
   source venv/bin/activate     # macOS/Linux
   # o en Windows PowerShell:
   # .\venv\Scripts\Activate.ps1
   ```
3. Instala dependencias:

   ```bash
   pip install -U yt-dlp
   ```
4. Verifica que `yt_dl.py` tenga permisos de ejecución:

   ```bash
   chmod +x yt_dl.py
   ```

---

## Uso

```bash
./yt_dl.py <URL o @archivo> [opciones]
```

### Argumentos

* `<URL o @archivo>`

  * Directamente la URL a descargar (YouTube, etc.).
  * Si comienza con `@`, se interpreta como un archivo de texto que contiene una URL por línea. Ejemplo: `@lista_urls.txt`.

### Opciones

* `-o, --output <directorio>`
  Directorio de salida donde se guardarán los archivos. Por defecto, carpeta actual (`.`). Si no existe, se crea.

* `--to-mp3`
  Activa la conversión a MP3. Si no se especifica, se guarda en formato original.

  * **Advertencia**: recodificar a MP3 implica pérdida adicional de calidad respecto al archivo original. Úsalo solo si tu reproductor no admite otros formatos.

* `--bitrate <kbps>`
  Bitrate para MP3 (solo si `--to-mp3` está activo). Valores comunes: `192`, `256`, `320`. Por defecto `320`.

* `-h, --help`
  Muestra ayuda de uso y sale.

### Ejemplos

1. **Descargar audio de una URL y guardar en formato original**, en el directorio actual:

   ```bash
   ./yt_dl.py "https://www.youtube.com/watch?v=XXXXXXXXXXX"
   ```

2. **Descargar y convertir a MP3 320 kbps**, guardando en carpeta `descargas`:

   ```bash
   ./yt_dl.py "https://www.youtube.com/watch?v=XXXXXXXXXXX" --to-mp3 -o descargas
   ```

3. **Descargar múltiples URLs listadas en un archivo `urls.txt`**:

   * Crear `urls.txt` con una URL por línea. Puedes añadir comentarios con `#` al inicio de la línea.
   * Ejecutar:

     ```bash
     ./yt_dl.py @urls.txt --to-mp3 -o descargas
     ```

4. **Descargar una playlist completa** (YouTube, etc.). Simplemente pasa la URL de la playlist:

   ```bash
   ./yt_dl.py "https://www.youtube.com/playlist?list=YYYYYYYYYYY" -o playlists/mi_playlist
   ```

   Si la playlist es larga, el script mostrará progreso por cada ítem y un resumen de cuántos ítems procesó.

---

## Explicación técnica y consideraciones

### Calidad de audio y recodificación

* **“Mejor calidad disponible”**: se refiere a la pista de audio de mayor bitrate o tecnología (Opus, AAC, etc.) que el sitio ofrezca.
* **Guardar en formato original** (`--to-mp3` no usado): con `format='bestaudio/best'`, `yt-dlp` descarga la pista sin recodificar, manteniendo la calidad “tal cual” está en el servidor.
* **Conversión a MP3**:

  * Hace uso de `FFmpegExtractAudio` de yt-dlp.
  * Por más alto que sea el bitrate (p.ej., 320 kbps), el proceso implica recodificación con pérdida, pues el audio original ya venía comprimido con pérdida.
  * Útil para compatibilidad con reproductores antiguos o dispositivos que no soporten Opus/AAC/WebM, pero no para “mejorar” calidad.
* **Recomendación**: si tu entorno reproduce `.m4a`, `.opus` o `.webm` correctamente, evita `--to-mp3` y conserva el original.

### Barra de progreso personalizada

* Se define una función `progreso_hook(d)` que recibe un diccionario `d` con información sobre la descarga:

  * `status`: `'downloading'`, `'finished'`, etc.
  * `downloaded_bytes`, `total_bytes` o `total_bytes_estimate`
  * `speed`, `eta`, etc.
* En cada llamada, se calcula porcentaje, tamaños en MiB, ETA en segundos y velocidad en KiB/s, mostrando en la misma línea.
* Cuando finaliza descarga de un ítem, muestra “Descarga completada, procesando...”.

### Manejo de playlists y múltiples URLs

* Si la URL apunta a una playlist, `info` resultante contendrá `entries`; el script:

  * Itera cada entrada.
  * Usa `ignoreerrors: True` para continuar si un ítem falla.
  * Al final informa cuántos ítems se procesaron con éxito (aproximado).
* Para archivos de URLs: usa prefijo `@archivo.txt`; lee líneas no vacías ni comentarios y procesa cada URL.

### Estructura con argparse

* Proporciona ayuda automática (`-h/--help`).
* Argumentos posicionale: URL o archivo.
* Opciones `-o/--output`, `--to-mp3`, `--bitrate`.

### Robustez y manejo de errores

* Se capturan excepciones de `yt-dlp` (`yt_dlp.utils.DownloadError`) para mostrar mensaje y continuar según corresponda.
* Otros errores genéricos también se capturan y reportan.
* Se valida lectura de archivo de URLs.

### Extensiones y personalización

* **Incrustar metadatos**: podrías añadir postprocesadores adicionales en `ydl_opts['postprocessors']`, por ejemplo:

  * `EmbedThumbnail`: para incrustar miniatura en MP3.
  * `FFmpegMetadata`: para incrustar tags ID3 (título, artista, álbum, etc.).
* **Logging**: actualmente se usa `quiet=True` y el progreso por hook. Para debugging, puedes quitar `quiet` y/o configurar un logger propio.
* **Bypass geográfico / Cookies**: yt-dlp permite opciones como `--geo-bypass`, `--cookies`, etc. Puedes exponerlas como opciones adicionales en el script si lo necesitas.
* **Soporte de proxies**: podrías permitir pasar variables de entorno o flags de yt-dlp para proxies HTTP/SOCKS.
* **Interfaz gráfica**: eventualmente envolver este script en una GUI (Tkinter, PyQt, Electron) si quieres una app de escritorio.
* **Integración con bases de datos**: guardar historial de descargas en SQLite, JSON o similar.

---

## Estructura del repositorio

```
yt-dl-audio/
├── yt_dl.py            # Script principal
├── README.md           # Este archivo
├── requirements.txt    # Opcional: listar dependencias, p.ej.:
                        # yt-dlp>=2025.xx
├── LICENSE             # Archivo de licencia (p.ej. MIT)
└── urls.txt.example    # Ejemplo de archivo con URLs para batch download
```

* **requirements.txt**: puedes incluir:

  ```
  yt-dlp>=2025.01.01
  ```

  (o la versión mínima que pruebes satisfactoria).
* **urls.txt.example**: un ejemplo con comentarios:

  ```
  # Lista de URLs a descargar:
  https://www.youtube.com/watch?v=XXXXXXXXXXX
  https://youtu.be/YYYYYYYYYYY
  # https://www.youtube.com/watch?v=ZZZZZZZZZZ  # esta línea está comentada
  ```
* **LICENSE**: MIT License.

---

## Contribuciones

1. Haz fork del repositorio.
2. Crea una rama (`git checkout -b feature/nueva-funcionalidad`).
3. Realiza cambios y pruebas.
4. Asegúrate de actualizar este README si añades opciones o comportamientos nuevos.
5. Envía un Pull Request describiendo detalladamente tu mejora o corrección.
6. Revisa y discute feedback. ¡Gracias por contribuir!

---

## Pruebas y validación

* Prueba con URLs individuales de YouTube, SoundCloud, Vimeo, etc.
* Prueba playlists largas y verifica que, ante errores (video removido o privado), el script continúa con los siguientes ítems.
* Verifica que la conversión a MP3 funciona solo si `ffmpeg` está presente, y muestra mensaje de error si no.
* Prueba con rutas de salida relativas y absolutas, incluyendo rutas con espacios o caracteres especiales.
* Verifica el comportamiento en Windows, macOS y Linux (diferencias en PATH, permisos, etc.).

---

## Ejemplo de uso en CI/CD o servidor

Si se desea automatizar descargas o ejecutar en un servidor headless:

* Crea un entorno virtual en el servidor.
* Instala dependencias: `pip install yt-dlp`.
* Asegúrate de instalar ffmpeg en el sistema.
* Escribe un cron job o script que invoque `yt_dl.py @urls.txt -o /ruta/descargas`:

  ```cron
  0 2 * * * /ruta/al/venv/bin/python /ruta/yt-dl-audio/yt_dl.py @/ruta/urls_actualizadas.txt -o /ruta/descargas/$(date +\%Y-\%m-\%d)
  ```
* Captura logs de salida en un archivo para revisión de errores:

  ```bash
  /ruta/venv/bin/python /ruta/yt-dl-audio/yt_dl.py ... >> /var/log/yt_dl.log 2>&1
  ```

---

## Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo `LICENSE` para más detalles.

```text
MIT License

Copyright (c) 2025 QuetziHack

Permission is hereby granted, free of charge, to any person obtaining a copy...
[Texto completo de la licencia MIT]
```

---

## Autor / Mantenimiento

* **Autor**: @QuetziHack.
* **Contacto**: pepeltorochdo@gmail.com.
* **Fecha**: Junio 2025.
* **Versión inicial actualizda**: 1.0.1.
