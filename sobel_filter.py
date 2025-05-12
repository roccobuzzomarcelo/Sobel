from PIL import Image
import numpy as np

def aplicar_sobel(imagen_path, output_path):
    """
    Aplica el operador de Sobel a una imagen para detectar bordes.

    Args:
        imagen_path (str): La ruta al archivo de imagen de entrada.
        output_path (str): La ruta donde se guardará la imagen con los bordes detectados.
    """
    try:
        # Abre la imagen
        img = Image.open(imagen_path).convert('L')  # Convertir a escala de grises
        ancho, alto = img.size
        imagen_np = np.array(img, dtype=np.int32)

        # Define las máscaras de Sobel
        mascara_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
        mascara_y = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])

        # Crea una imagen de salida con las mismas dimensiones
        bordes = np.zeros((alto, ancho), dtype=np.uint8)

        # Aplica las máscaras a cada píxel
        for y in range(1, alto - 1):
            for x in range(1, ancho - 1):
                ventana = imagen_np[y-1:y+2, x-1:x+2]

                # Convolución con las máscaras
                gx = np.sum(ventana * mascara_x)
                gy = np.sum(ventana * mascara_y)

                # Magnitud del gradiente (aproximación)
                magnitud = np.sqrt(gx**2 + gy**2)

                # Asegurar que el valor esté en el rango [0, 255]
                bordes[y, x] = np.clip(magnitud, 0, 255)

        # Crea una imagen PIL desde el array NumPy y la guarda
        imagen_bordes = Image.fromarray(bordes)
        imagen_bordes.save(output_path)
        print(f"Bordes detectados y guardados en: {output_path}")

    except FileNotFoundError:
        print(f"Error: No se encontró la imagen en la ruta: {imagen_path}")
    except Exception as e:
        print(f"Ocurrió un error: {e}")

if __name__ == "__main__":
    ruta_imagen_entrada = "image.jpg" 
    ruta_imagen_salida = "outputs/proccesed.jpg"
    aplicar_sobel(ruta_imagen_entrada, ruta_imagen_salida)