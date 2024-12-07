import cv2
import os

def process_video_intervals(video_path, output_folder, intervals, resolution=(28, 21)):
    """
    Procesa un video en intervalos específicos y guarda 4 imágenes repetidas por cada frame.

    Args:
        video_path (str): Ruta al video de entrada.
        output_folder (str): Carpeta para guardar los recortes.
        intervals (list): Lista de intervalos en segundos [(inicio1, fin1), (inicio2, fin2), ...].
        resolution (tuple): Resolución fija para las imágenes redimensionadas (ancho, alto).
    """
    os.makedirs(output_folder, exist_ok=True)
    
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: No se pudo abrir el video en {video_path}")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    crop_count = 0

    for start, end in intervals:
        cap.set(cv2.CAP_PROP_POS_MSEC, start * 1000)
        while cap.get(cv2.CAP_PROP_POS_MSEC) < end * 1000:
            ret, frame = cap.read()
            if not ret:
                break

            resized_frame = cv2.resize(frame, resolution, interpolation=cv2.INTER_AREA)
            for i in range(4):
                output_path = os.path.join(output_folder, f"frame_{crop_count:05d}_{i}.jpg")
                cv2.imwrite(output_path, resized_frame)
            
            crop_count += 1

    cap.release()
    print(f"Proceso completado. Imágenes redimensionadas: {crop_count * 4}")

# Definir los intervalos en segundos para cada video
intervals_porsche1 = [
    (2, 9),
    (12, 19),
    (27, 42),
    (47, 48),
    (57, 86),
    (152, 201),
    (300, 308)
]

intervals_porsche2 = [
    (28, 31),
    (34, 36),
    (40,45),
    (78, 88),
    (109, 112),
    (115, 118)
]

intervals_mercedes = [
    (41, 50),
    (54, 56),
    (68, 72),
    (92, 97),
    (101, 106),
    (132, 135)
]

# Rutas de los videos
video_path1 = r"C:\Users\luis2\OneDrive\Documentos\Escuela\Semestre 9\IA\IAProyectos\Proyecto3\VideoCars\PorscheGT3RS1.mp4"
video_path2 = r"C:\Users\luis2\OneDrive\Documentos\Escuela\Semestre 9\IA\IAProyectos\Proyecto3\VideoCars\PorscheGT3RS2.mp4"
video_path_mercedes = r"C:\Users\luis2\OneDrive\Documentos\Escuela\Semestre 9\IA\IAProyectos\Proyecto3\VideoCars\2025MercedesG63AMGFaceliftWhite.mp4"

# Carpeta de salida
output_folder_porsche = r"C:\Users\luis2\OneDrive\Documentos\Escuela\Semestre 9\IA\IAProyectos\Proyecto3\dataset\PorscheGT3RS"
output_folder_mercedes = r"C:\Users\luis2\OneDrive\Documentos\Escuela\Semestre 9\IA\IAProyectos\Proyecto3\dataset\MercedesG63AMGFacelift"

# Procesar los videos
process_video_intervals(video_path1, output_folder_porsche, intervals_porsche1)
process_video_intervals(video_path2, output_folder_porsche, intervals_porsche2)
process_video_intervals(video_path_mercedes, output_folder_mercedes, intervals_mercedes)