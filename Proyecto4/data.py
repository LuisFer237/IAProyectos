import warnings
import requests
import json
import whisper
import os
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

# Ignorar advertencias de whisper y torch
# warnings.filterwarnings("ignore", category=UserWarning, module="whisper")
# warnings.filterwarnings("ignore", category=FutureWarning, module="torch")

# Function to read text from a file
def read_text_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# Function to write text to a file
def write_text_to_file(file_path, text):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(text)

# Function to get synopsis from Llama server
def get_synopsis_from_llama(text):
    try:
        url = "http://localhost:1234/v1/completions"
        headers = {"Content-Type": "application/json"}
        payload = {
            "model": "llama-3.2-1b-instruct",
            "prompt": f"""
                A continuación, se presenta un documento que puede ser la transcripción de un video convertido a texto, un artículo, o un libro. Necesito un resumen detallado que contenga toda la información relevante y que sea claro y organizado. Sigue estas indicaciones según el tipo de documento:
                Si es un video:
                Resume los puntos clave discutidos en el video.
                Proporciona un breve contexto para cada punto clave.
                Incluye explícitamente información numérica o datos importantes si se mencionan.
                Destaca conclusiones, opiniones o propuestas presentadas en el video.
                Si es un artículo o un libro (especificado al inicio del texto):
                Identifica el tema principal y el propósito del documento.
                Resume los puntos clave o capítulos importantes, indicando su contexto.
                Incluye datos relevantes, citas textuales significativas, o ideas principales que refuercen el argumento central.
                Destaca las conclusiones, aportaciones o propuestas más relevantes.
                Texto original:
                {text}
                Por favor, crea un resumen preciso y fácil de entender, destacando toda la información esencial acorde al tipo de documento.
            """,
            "max_tokens": 40000
        }
        print("Enviando solicitud al servidor Llama...")
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()  # Verifica errores HTTP
        response_data = response.json()
        return response_data['choices'][0]['text']
    except requests.exceptions.RequestException as e:
        return f"Error al conectar con el servidor Llama: {e}"

# Function to transcribe audio using Whisper
def transcribe_audio(file_path):
    print("Transcribiendo audio...")
    model = whisper.load_model("base", device="cpu")
    result = model.transcribe(file_path)
    return result["text"]

# Function to process files
def process_files(file_paths, status_text):
    if not os.path.exists("Proyecto4/dataset"):
        os.makedirs("Proyecto4/dataset")
    
    for file_path in file_paths:
        file_name, file_extension = os.path.splitext(file_path)
        if file_extension.lower() in ['.mp4', '.wav', '.mp3']:
            status_text.insert(tk.END, f"Iniciando transcripción de audio para {file_path}...\n")
            text = transcribe_audio(file_path)
            status_text.insert(tk.END, "Transcripción completada. Obteniendo sinopsis del servidor Llama...\n")
        elif file_extension.lower() in ['.txt']:
            status_text.insert(tk.END, f"Leyendo archivo de texto {file_path}...\n")
            text = read_text_from_file(file_path)
        else:
            status_text.insert(tk.END, f"Tipo de archivo no soportado: {file_path}\n")
            continue
        
        synopsis = get_synopsis_from_llama(text)
        output_file = os.path.join("Proyecto4/dataset", f"{os.path.basename(file_name)}resumen.txt")
        status_text.insert(tk.END, f"Sinopsis obtenida. Escribiendo resultado al archivo de salida {output_file}...\n")
        write_text_to_file(output_file, synopsis)
        status_text.insert(tk.END, f"Proceso completado para {file_path}.\n")

# Function to open file dialog
def open_file_dialog(status_text):
    file_paths = filedialog.askopenfilenames(title="Seleccionar archivos", filetypes=[("Todos los archivos", "*.*")])
    if file_paths:
        process_files(file_paths, status_text)
        messagebox.showinfo("Proceso completado", "Todos los archivos han sido procesados y guardados en la carpeta 'dataset'.")

# Create the main window
root = tk.Tk()
root.title("Procesador de Archivos")
root.geometry("600x400")

# Create and place the button
btn_select_files = tk.Button(root, text="Seleccionar Archivos", command=lambda: open_file_dialog(status_text))
btn_select_files.pack(pady=20)

# Create and place the status text area
status_text = scrolledtext.ScrolledText(root, width=70, height=15)
status_text.pack(pady=10)

# Run the application
root.mainloop()