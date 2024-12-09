import cv2
import os

def process_video_intervals(video_path, output_folder, intervals, hsv_ranges, resolution=(28, 21)):
    """
    Procesa un video en intervalos específicos y guarda 4 imágenes repetidas por cada frame.

    Args:
        video_path (str): Ruta al video de entrada.
        output_folder (str): Carpeta para guardar los recortes.
        intervals (list): Lista de intervalos en segundos [(inicio1, fin1), (inicio2, fin2), ...].
        hsv_ranges (tuple): Rango de color HSV (lower, upper).
        resolution (tuple): Resolución fija para las imágenes redimensionadas (ancho, alto).
    """
    os.makedirs(output_folder, exist_ok=True)
    
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: No se pudo abrir el video en {video_path}")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    crop_count = 0

    lower_hsv, upper_hsv = hsv_ranges

    for start, end in intervals:
        cap.set(cv2.CAP_PROP_POS_MSEC, start * 1000)
        while cap.get(cv2.CAP_PROP_POS_MSEC) < end * 1000:
            ret, frame = cap.read()
            if not ret:
                break

            # Convertir el frame a HSV y aplicar la máscara de color
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv, lower_hsv, upper_hsv)
            mask = cv2.erode(mask, None, iterations=0)
            mask = cv2.dilate(mask, None, iterations=0)

            # Encontrar contornos en la máscara
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if contours:
                largest_contour = max(contours, key=cv2.contourArea)
                ((x, y), radius) = cv2.minEnclosingCircle(largest_contour)
                if radius > 10:
                    top_left = list((int(x - radius), int(y - radius)))
                    bottom_right = list((int(x + radius), int(y + radius)))

                    if top_left[0] < 0:
                        top_left[0] = 0
                    if top_left[1] < 0:
                        top_left[1] = 0

                    cropped_image = frame[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]
                    if cropped_image.size > 0:
                        resized_frame = cv2.resize(cropped_image, resolution, interpolation=cv2.INTER_AREA)
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

intervals_mercedes_white = [
    (41, 50),
    (54, 56),
    (68, 72),
    (92, 97),
    (101, 106),
    (132, 135)
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
    (21, 22),
    (29, 31),
    (86, 90),
    (112, 114),
    (121, 123)
]

# Rutas de los videos
video_path1 = r"C:\Users\luis2\OneDrive\Documentos\Escuela\Semestre 9\IA\IAProyectos\Proyecto3\VideoCars\PorscheGT3RS1.mp4"
video_path2 = r"C:\Users\luis2\OneDrive\Documentos\Escuela\Semestre 9\IA\IAProyectos\Proyecto3\VideoCars\PorscheGT3RS2.mp4"
video_path_mercedes_white = r"C:\Users\luis2\OneDrive\Documentos\Escuela\Semestre 9\IA\IAProyectos\Proyecto3\VideoCars\2025MercedesG63AMGFaceliftWhite.mp4"
video_path_mercedes_blue = r"C:\Users\luis2\OneDrive\Documentos\Escuela\Semestre 9\IA\IAProyectos\Proyecto3\VideoCars\MercedesBenzG63AMGFaceliftBlue.mp4"
video_path_mercedes_gray = r"C:\Users\luis2\OneDrive\Documentos\Escuela\Semestre 9\IA\IAProyectos\Proyecto3\VideoCars\MercedesG63AMGFaceliftGray.mp4"

# Carpeta de salida
output_folder_porsche = r"C:\Users\luis2\OneDrive\Documentos\Escuela\Semestre 9\IA\IAProyectos\Proyecto3\dataset\PorscheGT3RS"
output_folder_mercedes = r"C:\Users\luis2\OneDrive\Documentos\Escuela\Semestre 9\IA\IAProyectos\Proyecto3\dataset\MercedesG63AMGFacelift"

# Definir los rangos HSV para cada video
hsv_ranges_porsche1 = ((0, 97, 1), (179, 255, 233))
hsv_ranges_porsche2 = ((0, 97, 1), (179, 255, 233))
hsv_ranges_mercedes_white = ((0, 0, 200), (180, 20, 255))
hsv_ranges_mercedes_blue = ((100, 150, 0), (140, 255, 255))
hsv_ranges_mercedes_gray = ((0, 0, 50), (180, 50, 200))

# Procesar los videos
process_video_intervals(video_path1, output_folder_porsche, intervals_porsche1, hsv_ranges_porsche1)
process_video_intervals(video_path2, output_folder_porsche, intervals_porsche2, hsv_ranges_porsche2)
process_video_intervals(video_path_mercedes_white, output_folder_mercedes, intervals_mercedes_white, hsv_ranges_mercedes_white)
process_video_intervals(video_path_mercedes_blue, output_folder_mercedes, intervals_mercedes_blue, hsv_ranges_mercedes_blue)
process_video_intervals(video_path_mercedes_gray, output_folder_mercedes, intervals_mercedes_gray, hsv_ranges_mercedes_gray)