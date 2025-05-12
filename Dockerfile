# Imagen base oficial de Python
FROM python:alpine3.13-slim	

# Evita prompts interactivos
ENV DEBIAN_FRONTEND=noninteractive

# Directorio de trabajo
WORKDIR /app

# Copiamos el código fuente
COPY . /app

# Instalamos dependencias necesarias
RUN pip install --no-cache-dir pillow numpy

# Variable de entorno para controlar el número de procesos (se puede sobrescribir en tiempo de ejecución)
ENV NUM_PROCESOS=4
ENV TIMEOUT=5

# Comando por defecto
CMD ["python", "main.py"]
