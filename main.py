import os
import time
import numpy as np
from PIL import Image
import multiprocessing as mp
from sobel_filter import aplicar_sobel  # Función centralizada

# --- FUNCIONES GLOBALES ---

def aplicar_sobel_porcion(porcion):
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

def worker_task(idx, porcion, result_dict, timeout):
    try:
        # Simulación de fallo (opcional, quitar si no se usa)
        if os.environ.get("SIMULAR_FALLOS", "False") == "True" and idx == 0:
            time.sleep(timeout + 1)
        result_dict[idx] = aplicar_sobel_porcion(porcion)
    except Exception as e:
        result_dict[idx] = e

# --- FUNCIÓN PRINCIPAL ---

def aplicar_sobel_distribuido_tolerante(imagen_path, output_path, num_procesos=4, timeout=5, max_reintentos=2):
    try:
        tiempo_inicio = time.time()
        img = Image.open(imagen_path).convert('L')
        ancho, alto = img.size
        imagen_np = np.array(img, dtype=np.int32)

        porcion_alto = alto // num_procesos
        porciones = []
        for i in range(num_procesos):
            y_inicio = i * porcion_alto
            y_fin = (i + 1) * porcion_alto if i < num_procesos - 1 else alto
            porcion = (imagen_np[y_inicio:y_fin, :], y_inicio, y_fin, ancho)
            porciones.append((i, porcion))

        resultados = [None] * num_procesos
        intentos = [0] * num_procesos
        manager = mp.Manager()
        result_dict = manager.dict()
        tareas_pendientes = set(range(num_procesos))

        while tareas_pendientes:
            procesos = []
            for idx in list(tareas_pendientes):
                if intentos[idx] >= max_reintentos:
                    print(f"❌ Parte {idx} falló demasiadas veces. Se omite.")
                    tareas_pendientes.remove(idx)
                    continue

                p = mp.Process(target=worker_task, args=(idx, porciones[idx][1], result_dict, timeout))
                procesos.append((idx, p))
                p.start()
                print(f"🧪 Lanzado proceso para parte {idx} (intento {intentos[idx] + 1})")

            for idx, p in procesos:
                p.join(timeout)
                if p.is_alive():
                    print(f"⏱️ Tiempo agotado para parte {idx}, terminando proceso...")
                    p.terminate()
                    intentos[idx] += 1
                elif isinstance(result_dict.get(idx), Exception):
                    print(f"⚠️ Error en parte {idx}: {result_dict[idx]}")
                    intentos[idx] += 1
                else:
                    resultados[idx] = result_dict[idx]
                    tareas_pendientes.remove(idx)
                    print(f"✅ Parte {idx} completada.")

        bordes_total = np.zeros((alto, ancho), dtype=np.uint8)
        for res in resultados:
            if res is None:
                continue
            bordes_porcion, y_inicio, y_fin = res
            bordes_total[y_inicio+1:y_fin-1, 1:ancho-1] = bordes_porcion[1:-1, 1:-1]

        Image.fromarray(bordes_total).save(output_path)
        tiempo_fin = time.time()
        print(f"🖼️ Imagen guardada en: {output_path}")
        print(f"🕒 Tiempo total: {tiempo_fin - tiempo_inicio:.2f} s")

    except FileNotFoundError:
        print(f"❌ Imagen no encontrada: {imagen_path}")
    except Exception as e:
        print(f"❌ Error general: {e}")


def aplicar_sobel_centralizado_con_tiempo(imagen_path, output_path):
    tiempo_inicio = time.time()
    aplicar_sobel(imagen_path, output_path)
    tiempo_fin = time.time()
    print(f"🕒 Tiempo (centralizado): {tiempo_fin - tiempo_inicio:.2f} s")

# --- ENTRY POINT ---
if __name__ == "__main__":
    ruta_imagen_entrada = "image.jpg"
    ruta_salida_distribuido = "outputs/bordes_distribuido.jpg"
    ruta_salida_centralizado = "outputs/bordes_centralizado.jpg"

    num_procesos = int(os.getenv("NUM_PROCESOS", 4))
    timeout = int(os.getenv("TIMEOUT", 5))

    print(f"🔧 Procesos: {num_procesos} | Timeout: {timeout}s")
    aplicar_sobel_distribuido_tolerante(ruta_imagen_entrada, ruta_salida_distribuido, num_procesos, timeout)
    aplicar_sobel_centralizado_con_tiempo(ruta_imagen_entrada, ruta_salida_centralizado)
