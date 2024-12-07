import cv2
import numpy as np

def pick_color(image_path):
    """
    Permite seleccionar un color en una imagen y devuelve su valor HSV.

    Args:
        image_path (str): Ruta a la imagen.
    """
    def mouse_callback(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            pixel = image[y, x]
            # Convertir BGR a HSV
            hsv_pixel = cv2.cvtColor(np.uint8([[pixel]]), cv2.COLOR_BGR2HSV)[0][0]
            print(f"HSV: {hsv_pixel}")

    # Cargar imagen
    image = cv2.imread(image_path)
    
    # Verificar si la imagen se cargó correctamente
    if image is None:
        print(f"Error: No se pudo abrir o leer el archivo de imagen en {image_path}")
        return

    # Redimensionar la imagen
    scale_percent = 50  # Porcentaje del tamaño original
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)
    image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

    cv2.imshow("Image", image)
    cv2.setMouseCallback("Image", mouse_callback)

    print("Haz clic en cualquier parte de la imagen para obtener el color HSV.")
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Llamar a la función con la ruta de la imagen
pick_color(r'C:\Users\luis2\OneDrive\Documentos\Escuela\Semestre 9\IA\IAProyectos\Proyecto3\car.png')