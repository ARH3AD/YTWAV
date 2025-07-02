import os
import yt_dlp
import flet as ft


# Ruta de salida de los archivos WAV
OUTPUT_DIR = os.path.join(os.path.expanduser("~"), "Downloads", "WAV Downloads")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Crea el directorio si no existe
os.makedirs(OUTPUT_DIR, exist_ok=True)


def descargar_y_convertir(url, tiempo, output_area):
    # Formatear el tiempo (ej. 1:29 -> 1 29)
    tiempo_formateado = tiempo.replace(":", " ")

    # Opciones de yt-dlp
    ydl_opts = {
        'format': 'bestaudio/best',  # Obtén el mejor audio posible
        'outtmpl': os.path.join(OUTPUT_DIR, f'%(title)s ({tiempo_formateado}).%(ext)s'),  # Ruta de salida con tiempo
        'postprocessors': [{  # Postprocesador para convertir a WAV
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',  # Convertir a WAV
        }],
        'ffmpeg_location': '/usr/local/bin/ffmpeg',  # Ruta explícita a FFmpeg
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            output_area.value += f"\nDescargando y convirtiendo: {url}"
            output_area.update()
            ydl.download([url])
        output_area.value += f"\n¡Descarga y conversión completadas para: {url}!"
        output_area.update()
    except Exception as e:
        output_area.value += f"\nError al procesar el enlace {url}: {e}"
        output_area.update()


def main(page: ft.Page):
    # Configuración de la ventana
    page.title = "Descargador WAV"
    page.scroll = ft.ScrollMode.AUTO

    # Elementos de la interfaz
    input_area = ft.TextField(
        label="Pega aquí los enlaces con tiempos:",
        multiline=True,
        expand=True,
        height=200,
    )

    output_area = ft.Text(
        value="Estado de descargas:",
        expand=True,
        selectable=True,
        height=200,
        width=500,
        style=ft.TextStyle(color="blue"),
    )

    progress_bar = ft.ProgressBar(value=0, width=500)
    download_button = ft.ElevatedButton("Iniciar Descargas", icon=ft.icons.DOWNLOAD)

    # Lógica del botón
    def iniciar_descarga(e):
        enlaces = input_area.value.strip().split("\n")
        total = len(enlaces)
        descargados = 0

        for line in enlaces:
            try:
                tiempo, url = line.strip().split(maxsplit=1)
                descargar_y_convertir(url, tiempo, output_area)
                descargados += 1
                progress_bar.value = descargados / total
                progress_bar.update()
            except ValueError:
                output_area.value += f"\nFormato incorrecto en la línea: {line.strip()}"
                output_area.update()

    download_button.on_click = iniciar_descarga

    # Añadir elementos a la página
    page.add(
        input_area,
        download_button,
        progress_bar,
        output_area,
    )


# Iniciar la aplicación Flet
if __name__ == "__main__":
    ft.app(target=main)
