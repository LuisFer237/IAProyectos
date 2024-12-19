import os
import csv
import yt_dlp
import openai
import whisper
import requests
import json
import re

# Configura tu clave de API de OpenAI
openai.api_key = 'TU_CLAVE_DE_API'

# Ruta del archivo CSV
csv_file_path = r'Proyecto4\YouTube Video List Scraper.csv'
audio_output_dir = r'Proyecto4\audios'
text_output_dir = r'Proyecto4\audios-texto'
summary_output_dir = r'Proyecto4\dataset'

# Máximo de videos a procesar
max_videos = 50

# Crear los directorios de salida si no existen
os.makedirs(audio_output_dir, exist_ok=True)
os.makedirs(text_output_dir, exist_ok=True)
os.makedirs(summary_output_dir, exist_ok=True)

def sanitize_filename(filename):
    filename = re.sub(r'[\\/*?:"<>|]', '_', filename)
    filename = filename.replace(' ', '')
    return filename

# Función para descargar el audio de un video de YouTube
def download_audio(video_url, output_dir, sanitized_title):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(output_dir, f'{sanitized_title}.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

# Función para transcribir audio usando OpenAI Whisper
def transcribe_audio(file_path):
    model = whisper.load_model("base")
    result = model.transcribe(file_path)
    return result['text']

# Función para obtener sinopsis del servidor Llama
def get_synopsis_from_llama(text):
    try:
        url = "http://localhost:1234/v1/completions"
        headers = {"Content-Type": "application/json"}
        payload = {
            "model": "llama-3.2-1b-instruct",
            "prompt": f"""
                A continuación, se presenta un documento que puede ser la transcripción de un video convertido a texto. Necesito un resumen detallado que contenga toda la información relevante y que sea claro y organizado

                Resume los puntos clave discutidos en el video.
                Proporciona un breve contexto para cada punto clave.
                Incluye explícitamente información numérica o datos importantes si se mencionan.
                Destaca conclusiones, opiniones o propuestas presentadas en el video.

                Texto original:
                {text}
                Por favor, crea un resumen preciso y fácil de entender, toma en cuenta que se usara para entrenar a un modelo de lenguaje a traves de embeding.
            """,
            "max_tokens": 1000
        }
        print("Enviando solicitud al servidor Llama...")
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()  # Verifica errores HTTP
        response_data = response.json()
        return response_data['choices'][0]['text']
    except requests.exceptions.RequestException as e:
        return f"Error al conectar con el servidor Llama: {e}"

# Leer el archivo CSV y procesar los primeros max_videos
with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    rows = list(reader)

videos_processed = 0
for row in rows:
    if videos_processed >= max_videos:
        break
    video_url = row['Video_Link']
    
    # Obtener el nombre del archivo descargado y limpiarlo
    sanitized_title = sanitize_filename(row['Video_Title'].strip())
    file_name = os.path.join(audio_output_dir, f"{sanitized_title}.mp3")
    
    print(f"Descargando audio de {video_url}...")
    download_audio(video_url, audio_output_dir, sanitized_title)
    
    # Verificar si el archivo de audio se descargó correctamente
    if os.path.exists(file_name):
        print(f"Transcribiendo audio de {file_name}...")
        text = transcribe_audio(file_name)
        
        # Guardar la transcripción en un archivo de texto y limpiarlo
        output_file = os.path.join(text_output_dir, f"{sanitized_title}_transcription.txt")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"Transcripción guardada en {output_file}")
        
        # Obtener sinopsis del texto transcrito
        print(f"Obteniendo sinopsis de {output_file}...")
        synopsis = get_synopsis_from_llama(text)
        
        # Guardar la sinopsis en un archivo de texto y limpiarlo
        summary_file = os.path.join(summary_output_dir, f"{sanitized_title}_summary.txt")
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(synopsis)
        print(f"Sinopsis guardada en {summary_file}")
        
        # Eliminar el registro del archivo CSV
        rows.remove(row)
        with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=row.keys())
            writer.writeheader()
            writer.writerows(rows)
    else:
        print(f"Error: No se encontró el archivo de audio {file_name}")
    
    videos_processed += 1