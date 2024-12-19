import cv2
import os
import numpy as np

def ajustar_brillo_contraste(frame, alpha=1.0, beta=0):
    return cv2.convertScaleAbs(frame, alpha=alpha, beta=beta)

def aplicar_zoom(frame, factor=1.2):
    h, w = frame.shape[:2]
    nh, nw = int(h / factor), int(w / factor)
    frame_zoom = frame[(h - nh) // 2:(h + nh) // 2, (w - nw) // 2:(w + nw) // 2]
    return cv2.resize(frame_zoom, (w, h))

def rotar_y_redimensionar(frame, angulo_max=15, resolution=(28, 21)):
    h, w = resolution
    centro = (w // 2, h // 2)
    angulo = np.random.uniform(-angulo_max, angulo_max)
    matriz_rotacion = cv2.getRotationMatrix2D(centro, angulo, 1)
    imagen_rotada = cv2.warpAffine(frame, matriz_rotacion, resolution)
    return imagen_rotada

def desenfoque_gaussiano(frame, kernel_size=(5, 5)):
    return cv2.GaussianBlur(frame, kernel_size, 0)

def agregar_ruido(frame, cantidad=0.02):
    h, w = frame.shape[:2]
    salida = np.copy(frame)
    num_pixeles = int(cantidad * h * w)
    for _ in range(num_pixeles):
        x, y = np.random.randint(0, w), np.random.randint(0, h)
        salida[y, x] = np.random.choice([0, 255], size=3)
    return salida

def aplicar_filtros(frame):
    filtros = {
        "brillo_alto": lambda img: ajustar_brillo_contraste(img, alpha=1.5, beta=30),
        "brillo_bajo": lambda img: ajustar_brillo_contraste(img, alpha=0.8, beta=-30),
        "zoom": lambda img: aplicar_zoom(img, factor=1.3),
        "desenfoque": lambda img: desenfoque_gaussiano(img),
        "ruido": lambda img: agregar_ruido(img),
    }

    resultados = {}
    for nombre, funcion in filtros.items():
        resultados[nombre] = funcion(frame)
    return resultados

def process_video_intervals(video_path, output_folder, intervals, max_frames, resolution=(28, 21)):
    os.makedirs(output_folder, exist_ok=True)
    total_frames = 0
    max_frames = min(max_frames, 400)

    while total_frames < max_frames:
        cap = cv2.VideoCapture(video_path)

        if not cap.isOpened():
            print(f"Error: No se pudo abrir el video en {video_path}")
            return

        frame_count = 0
        frame_skip = 3  # Tomar 1 de cada 3 frames
        for start, end in intervals:
            cap.set(cv2.CAP_PROP_POS_MSEC, start * 1000)
            while cap.get(cv2.CAP_PROP_POS_MSEC) < end * 1000 and total_frames < max_frames:
                ret, frame = cap.read()
                if not ret:
                    break

                if frame_count % frame_skip == 0:
                    current_time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000
                    resized_frame = cv2.resize(frame, resolution, interpolation=cv2.INTER_AREA)

                    # Guardar el frame original redimensionado
                    output_path = os.path.join(output_folder, f"frame_{total_frames:05d}_original_{current_time:.2f}.jpg")
                    cv2.imwrite(output_path, resized_frame)

                    # Aplicar rotaciones
                    for angle in [15, -15]:
                        rotated_frame = rotar_y_redimensionar(resized_frame, angulo_max=angle, resolution=resolution)
                        output_path = os.path.join(output_folder, f"frame_{total_frames:05d}_rot_{angle}_{current_time:.2f}.jpg")
                        cv2.imwrite(output_path, rotated_frame)

                    # Aplicar filtros
                    filtros_aplicados = aplicar_filtros(resized_frame)
                    for nombre, img_filtrada in filtros_aplicados.items():
                        output_path = os.path.join(output_folder, f"frame_{total_frames:05d}_{nombre}_{current_time:.2f}.jpg")
                        cv2.imwrite(output_path, img_filtrada)

                    total_frames += 1
                    if total_frames >= max_frames:
                        break

                frame_count += 1

        cap.release()
        print(f"Proceso completado. Total de frames procesados en esta iteración: {frame_count}")

    print(f"Proceso completado. Total de frames procesados: {total_frames}")

# Definir el número máximo de frames a procesar por video
max_frames = 400

# Definir los intervalos en segundos para cada video
intervals_porsche_amarillo = [
    (9, 9),
    (20, 21),
    (29, 30),
    (34, 36),
    (40, 42),
    (45, 45),
    (65, 68),
    (79, 80),
    (87, 88),
    (109, 110),
    (114, 117),
]

intervals_porsche_blanco = [
    (19, 20),
    (25, 27),
    (36, 40),
    (50, 51),
    (56, 57),
    (98, 101),
    (132, 134),
    (141, 141)
]

intervals_porsche_negro = [
    (5, 8),
    (18, 32),
    (37, 37),
    (40, 41),
    (55, 56),
    (61, 62),
    (72, 74),
    (123, 124)
]

intervals_porsche_azul = [
    (15, 16),
    (19, 20),
    (23, 23),
    (49, 50),
    (62, 63),
    (82, 82),
]

intervals_g63_blanco = [
    (40, 41),
    (53, 55),
    (70, 71),
    (73, 73),
    (95, 96),
    (124, 125),
    (133, 135)
]

intervals_g63_azul = [
    (18, 18),
    (36, 36),
    (50, 51),
    (58, 58),
    (61, 61),
    (66, 68),
    (114, 114),
    (152, 154),
    (181, 185)
]

intervals_g63_gris = [
    (3, 4),
    (7, 8),
    (22, 22),
    (29, 31),
    (86, 90),
    (106, 106),
    (112, 112),
    (121, 123)
]

intervals_g63_negro = [
    (2, 4),
    (17, 17),
    (26, 26),
    (50, 52),
    (71, 71),
    (105, 105),
    (109, 110),
    (117, 118)
]

intervals_urus_amarillo = [
    (16, 19),
    (33, 34),
    (38, 38),
    (42, 43),
    (49, 53),
    (142, 143),
    (185, 190)
]

intervals_urus_azul = [
    (1, 6),
    (23, 24),
    (33, 34),
    (40, 40),
    (45, 45),
    (49, 55),
    (70, 74),
    (163, 164),
    (190, 193),
    (243, 247)
]

intervals_urus_negro = [
    (32, 34),
    (41, 42),
    (49, 53),
    (58, 59),
    (62, 63),
    (66, 66),
    (69, 70),
    (73, 74),
    (76, 78),
    (120, 122)
]

intervals_urus_verde = [
    (38, 39),
    (46, 47),
    (56, 57),
    (61, 61),
    (67, 71),
    (76, 77),
    (82, 82)
]

intervals_812competizione_azul = [
    (42, 43),
    (52, 52),
    (57, 57),
    (62, 67),
    (71, 71),
    (78, 78),
    (114, 116),
    (134, 134),
    (145, 145)
]

intervals_812competizione_blanco = [
    (15, 17),
    (26, 27),
    (37, 37),
    (39, 41),
    (44, 47),
    (66, 75)
]

intervals_812competizione_gris = [
    (5, 7),
    (12, 13),
    (29, 30),
    (48, 48),
    (56, 57),
    (64, 64),
    (94, 95),
    (107, 107)
]

intervals_812competizione_rojo = [
    (33, 33),
    (41, 41),
    (46, 47),
    (90, 90),
    (101, 101),
    (107, 107),
    (126, 130)
]

intervals_uracansto_amarillo = [
    (1, 3),
    (17, 18),
    (22, 23),
    (33, 33),
    (36, 44),
    (55, 56),
    (81, 83),
    (143, 151)
]

intervals_uracansto_morado = [
    (4, 5),
    (18, 21),
    (33, 33),
    (49, 54),
    (94, 96),
    (121, 128)
]

intervals_uracansto_negro = [
    (2, 3),
    (16, 16),
    (22, 22),
    (26, 26),
    (32, 37),
    (132, 139)
]

intervals_uracansto_verde = [
    (8, 9),
    (24, 28),
    (32, 33),
    (38, 40),
    (53, 57),
    (67, 72),
    (152, 157)
]

# Rutas de los videos
video_path_amarillo = r"Proyecto3\VideoCars\PorscheGT3RS2_Amarillo.mp4"
video_path_blanco = r"Proyecto3\VideoCars\PorscheGT3RS2_Blanco.mp4"
video_path_negro = r"Proyecto3\VideoCars\PorscheGT3RS2_Negro.mp4"
video_path_azul = r"Proyecto3\VideoCars\PorscheGT3RS2_Azul.mp4"
video_path_g63_blanco = r"Proyecto3\VideoCars\G63AMGFacelift_Blanco.mp4"
video_path_g63_azul = r"Proyecto3\VideoCars\G63AMGFacelift_Azul.mp4"
video_path_g63_gris = r"Proyecto3\VideoCars\G63AMGFacelift_Gris.mp4"
video_path_g63_negro = r"Proyecto3\VideoCars\G63AMGFacelift_Negro.mp4"
video_path_urus_amarillo = r"Proyecto3\VideoCars\UrusS_Amarillo.mp4"
video_path_urus_azul = r"Proyecto3\VideoCars\UrusS_Azul.mp4"
video_path_urus_negro = r"Proyecto3\VideoCars\UrusS_Negro.mp4"
video_path_urus_verde = r"Proyecto3\VideoCars\UrusS_Verde.mp4"
video_path_812competizione_azul = r"Proyecto3\VideoCars\812Competizione_Azul.mp4"
video_path_812competizione_blanco = r"Proyecto3\VideoCars\812Competizione_Blanco.mp4"
video_path_812competizione_gris = r"Proyecto3\VideoCars\812Competizione_Gris.mp4"
video_path_812competizione_rojo = r"Proyecto3\VideoCars\812Competizione_Rojo.mp4"
video_path_huracansto_amarillo = r"Proyecto3\VideoCars\HuracanSTO_Amarillo.mp4"
video_path_huracansto_morado = r"Proyecto3\VideoCars\HuracanSTO_Morado.mp4"
video_path_huracansto_negro = r"Proyecto3\VideoCars\HuracanSTO_Negro.mp4"
video_path_huracansto_verde = r"Proyecto3\VideoCars\HuracanSTO_Verde.mp4"

# Carpeta de salida
output_folder_porsche = r"Proyecto3\dataset\PorscheGT3RS"
output_folder_g63 = r"Proyecto3\dataset\G63AMGFacelift"
output_folder_urus = r"Proyecto3\dataset\Urus"
output_folder_812competizione = r"Proyecto3\dataset\812Competizione"
output_folder_huracansto = r"Proyecto3\dataset\UracanSTO"

# Procesar los videos
process_video_intervals(video_path_amarillo, output_folder_porsche, intervals_porsche_amarillo, max_frames)
process_video_intervals(video_path_blanco, output_folder_porsche, intervals_porsche_blanco, max_frames)
process_video_intervals(video_path_negro, output_folder_porsche, intervals_porsche_negro, max_frames)
process_video_intervals(video_path_azul, output_folder_porsche, intervals_porsche_azul, max_frames)

process_video_intervals(video_path_g63_blanco, output_folder_g63, intervals_g63_blanco, max_frames)
process_video_intervals(video_path_g63_azul, output_folder_g63, intervals_g63_azul, max_frames)
process_video_intervals(video_path_g63_gris, output_folder_g63, intervals_g63_gris, max_frames)
process_video_intervals(video_path_g63_negro, output_folder_g63, intervals_g63_negro, max_frames)

process_video_intervals(video_path_urus_amarillo, output_folder_urus, intervals_urus_amarillo, max_frames)
process_video_intervals(video_path_urus_azul, output_folder_urus, intervals_urus_azul, max_frames)
process_video_intervals(video_path_urus_negro, output_folder_urus, intervals_urus_negro, max_frames)
process_video_intervals(video_path_urus_verde, output_folder_urus, intervals_urus_verde, max_frames)

process_video_intervals(video_path_812competizione_azul, output_folder_812competizione, intervals_812competizione_azul, max_frames)
process_video_intervals(video_path_812competizione_blanco, output_folder_812competizione, intervals_812competizione_blanco, max_frames)
process_video_intervals(video_path_812competizione_gris, output_folder_812competizione, intervals_812competizione_gris, max_frames)
process_video_intervals(video_path_812competizione_rojo, output_folder_812competizione, intervals_812competizione_rojo, max_frames)

process_video_intervals(video_path_huracansto_amarillo, output_folder_huracansto, intervals_uracansto_amarillo, max_frames)
process_video_intervals(video_path_huracansto_morado, output_folder_huracansto, intervals_uracansto_morado, max_frames)
process_video_intervals(video_path_huracansto_negro, output_folder_huracansto, intervals_uracansto_negro, max_frames)
process_video_intervals(video_path_huracansto_verde, output_folder_huracansto, intervals_uracansto_verde, max_frames)