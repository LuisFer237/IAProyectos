import cv2
import os
import uuid

def process_video_intervals(video_path, output_folder, intervals, resolution=(28, 21)):
    """
    Procesa un video en intervalos específicos y guarda imágenes repetidas y rotadas por cada frame.

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

            current_time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000
            resized_frame = cv2.resize(frame, resolution, interpolation=cv2.INTER_AREA)
            for i in range(3):
                unique_id = uuid.uuid4().hex
                output_path = os.path.join(output_folder, f"frame_{crop_count:05d}_{i}_{current_time:.2f}.jpg")
                cv2.imwrite(output_path, resized_frame)
            
            # Crear imágenes rotadas
            for angle in [15, -15]:  # Rotar 15 grados y -15 grados
                M = cv2.getRotationMatrix2D((resolution[0] / 2, resolution[1] / 2), angle, 1)
                rotated_frame = cv2.warpAffine(resized_frame, M, resolution)
                unique_id = uuid.uuid4().hex
                output_path = os.path.join(output_folder, f"frame_{crop_count:05d}_rot_{angle}_{current_time:.2f}.jpg")
                cv2.imwrite(output_path, rotated_frame)
            
            crop_count += 1

    cap.release()
    print(f"Proceso completado. Imágenes redimensionadas y rotadas: {crop_count * 5}")

# Definir los intervalos en segundos para cada video
intervals_mini_cooper = [
    (2, 9),
    (12, 19),
    (27, 42),
    (47, 48),
    (57, 86),
    (152, 201),
    (300, 308)
]

intervals_porsche_cayenne = [
    (28, 31),
    (34, 36),
    (40, 45),
    (78, 88),
    (109, 112),
    (115, 118)
]

intervals_fiat_panda = [
    (41, 50),
    (54, 56),
    (68, 72),
    (92, 97),
    (101, 106),
    (132, 135)
]

intervals_porsche1 = [
    (2, 9),
    (12, 19),
    (28, 42),
    (47, 48),
    (57,68),
    (75,86),
    (152, 201),
    (300, 308)
]

intervals_porsche2 = [
    (28, 31),
    (34, 36),
    (40, 45),
    (78, 88),
    (109, 112),
    (115, 118)
]

intervals_mercedes_white = [
    (41, 50),
    (54, 56),
    (68, 72),
    (92, 97),
    (101, 106),
    (133, 135)
]

intervals_mercedes_blue = [
    (10, 11),
    (18, 20),
    (34, 36),
    (49, 54),
    (58, 62),
    (66, 68),
    (112, 114),
    (181, 185)
]

intervals_mercedes_gray = [
    (3, 4),
    (7, 8),
    (29, 31),
    (86, 90),
    (112, 114),
    (121, 123)
]

intervals_volkswagen_id_buzz = [
    (5, 18),
    (25, 28),
    (37, 38),
    (44, 77),
    (101, 110)
]

# Rutas de los videos
video_path1 = r"C:\Users\luis2\OneDrive\Documentos\Escuela\Semestre 9\IA\IAProyectos\Proyecto3\VideoCars\PorscheGT3RS1.mp4"
video_path2 = r"C:\Users\luis2\OneDrive\Documentos\Escuela\Semestre 9\IA\IAProyectos\Proyecto3\VideoCars\PorscheGT3RS2.mp4"
video_path_mercedes_white = r"C:\Users\luis2\OneDrive\Documentos\Escuela\Semestre 9\IA\IAProyectos\Proyecto3\VideoCars\2025MercedesG63AMGFaceliftWhite.mp4"
video_path_mercedes_blue = r"C:\Users\luis2\OneDrive\Documentos\Escuela\Semestre 9\IA\IAProyectos\Proyecto3\VideoCars\MercedesBenzG63AMGFaceliftBlue.mp4"
video_path_mercedes_gray = r"C:\Users\luis2\OneDrive\Documentos\Escuela\Semestre 9\IA\IAProyectos\Proyecto3\VideoCars\MercedesG63AMGFaceliftGray.mp4"
video_path_volkswagen_id_buzz = r"C:\Users\luis2\OneDrive\Documentos\Escuela\Semestre 9\IA\IAProyectos\Proyecto3\VideoCars\2025 Volkswagen ID. Buzz Pomelo Yellow.mp4"

# Carpeta de salida

output_folder_porsche = r"C:\Users\luis2\OneDrive\Documentos\Escuela\Semestre 9\IA\IAProyectos\Proyecto3\dataset\PorscheGT3RS"
output_folder_mercedes = r"C:\Users\luis2\OneDrive\Documentos\Escuela\Semestre 9\IA\IAProyectos\Proyecto3\dataset\MercedesG63AMGFacelift"
output_folder_volkswagen_id_buzz = r"C:\Users\luis2\OneDrive\Documentos\Escuela\Semestre 9\IA\IAProyectos\Proyecto3\dataset\VolkswagenIDBuzz"

# Procesar los videos

process_video_intervals(video_path1, output_folder_porsche, intervals_porsche1)
process_video_intervals(video_path2, output_folder_porsche, intervals_porsche2)
process_video_intervals(video_path_mercedes_white, output_folder_mercedes, intervals_mercedes_white)
process_video_intervals(video_path_mercedes_blue, output_folder_mercedes, intervals_mercedes_blue)
process_video_intervals(video_path_mercedes_gray, output_folder_mercedes, intervals_mercedes_gray)
process_video_intervals(video_path_volkswagen_id_buzz, output_folder_volkswagen_id_buzz, intervals_volkswagen_id_buzz)