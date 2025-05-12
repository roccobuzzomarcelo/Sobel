from PIL import Image
import numpy as np
import multiprocessing as mp
import time

def aplicar_sobel_porcion(porcion):
    """
    Aplica el operador de Sobel a una porción de la imagen.

    Args:
        porcion (tuple): Una tupla que contiene la porción de la imagen (array NumPy),
                         y las coordenadas (y_inicio, y_fin) de esta porción en la imagen original.

    Returns:
        tuple: Una tupla que contiene la porción de los bordes detectados (array NumPy)
               y las coordenadas (y_inicio, y_fin).
    """
    imagen_np, y_inicio, y_fin, ancho = porcion
    alto_porcion = y_fin - y_inicio
    bordes_porcion = np.zeros((alto_porcion, ancho), dtype=np.uint8)
    mascara_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    mascara_y = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])

    for y in range(1, alto_porcion - 1):
        for x in range(1, ancho - 1):
            ventana = imagen_np[y-1:y+2, x-1:x+2]

            gx = np.sum(ventana * mascara_x)
            gy = np.sum(ventana * mascara_y)
            magnitud = np.sqrt(gx**2 + gy**2)
            bordes_porcion[y, x] = np.clip(magnitud, 0, 255)

    return bordes_porcion, y_inicio, y_fin

def aplicar_sobel_distribuido(imagen_path, output_path, num_procesos):
    """
    Aplica el operador de Sobel a una imagen de manera distribuida utilizando múltiples procesos.

    Args:
        imagen_path (str): La ruta al archivo de imagen de entrada.
        output_path (str): La ruta donde se guardará la imagen con los bordes detectados.
        num_procesos (int): El número de procesos a utilizar.
    """
    try:
        tiempo_inicio = time.time()
        img = Image.open(imagen_path).convert('L')
        ancho, alto = img.size
        imagen_np = np.array(img, dtype=np.int32)

        # Divide la imagen en porciones
        porcion_alto = alto // num_procesos
        porciones = []
        for i in range(num_procesos):
            y_inicio = i * porcion_alto
            y_fin = (i + 1) * porcion_alto if i < num_procesos - 1 else alto
            porcion = (imagen_np[y_inicio:y_fin, :], y_inicio, y_fin, ancho)
            porciones.append(porcion)

        # Crea un pool de procesos
        with mp.Pool(processes=num_procesos) as pool:
            resultados = pool.map(aplicar_sobel_porcion, porciones)

        # Unifica los resultados
        bordes_total = np.zeros((alto, ancho), dtype=np.uint8)
        for bordes_porcion, y_inicio, y_fin in resultados:
            bordes_total[y_inicio+1:y_fin-1, 1:ancho-1] = bordes_porcion[1:bordes_porcion.shape[0]-1, 1:bordes_porcion.shape[1]-1]

        # Crea la imagen de salida y la guarda
        imagen_bordes = Image.fromarray(bordes_total)
        imagen_bordes.save(output_path)
        tiempo_fin = time.time()
        print(f"Bordes detectados (distribuido con {num_procesos} procesos) y guardados en: {output_path}")
        print(f"Tiempo de ejecución: {tiempo_fin - tiempo_inicio:.4f} segundos")

    except FileNotFoundError:
        print(f"Error: No se encontró la imagen en la ruta: {imagen_path}")
    except Exception as e:
        print(f"Ocurrió un error: {e}")

if __name__ == "__main__":
    ruta_imagen_entrada = "image.jpg"
    ruta_imagen_salida_distribuida = "outputs/bordes_detectados_distribuido.jpg"
    num_procesos_a_probar = [1, 2, 4, 8]

    for num_procesos in num_procesos_a_probar:
        aplicar_sobel_distribuido(ruta_imagen_entrada, f"outputs/bordes_{num_procesos}_procesos.jpg", num_procesos)
