# Trabajo Práctico Nº 3

## Computación en la Nube (Kubernetes / RabbitMQ)

### HIT 1

**El operador de Sobel** es una máscara que, aplicada a una imagen, permite detectar (resaltar) bordes. Este operador es una operación matemática que, aplicada a cada pixel y teniendo en cuenta los píxeles que lo rodean, obtiene un nuevo valor (color) para ese pixel. Aplicando la operación a cada píxel, se obtiene una nueva imagen que resalta los bordes.

Objetivo:

- Input: una imagen.
- proceso (Sobel).
- output: una imagen filtrada.

**Parte 1:**

- Desarrollar un proceso centralizado que tome una imagen, aplique la máscara, y genere un nuevo archivo con el resultado.

* * *

#### **Resolucion - Parte 1**

El operador de Sobel utiliza dos máscaras (kernels)
una para detectar cambios horizontales y otra para detectar cambios verticales y combina estas magnitudes para resaltar los bordes de la imagen. Las matrices clásicas son:

```python
Gx (cambios horizontales):
    -1  0  1
    -2  0  2
    -1  0  1
```

```python
Gy (cambios verticales):
     1  2  1
     0  0  0
    -1 -2 -1
```

Nosotros lo resolvimos a tráves de la función ```sobel_filter.py``` que se va a encargar de tomar una imagen, convertirla a escala de grises. Luego utiliza las máscaras de Sobel (horizontal y vertical) para calcular la magnitud del cambio de intensidad (gradiente) en cada píxel. Esta magnitud representa la fuerza del borde. Finalmente, guarda una nueva imagen donde la intensidad de cada píxel corresponde a la magnitud del borde detectado en la imagen original.

Para poder probarlo utilizamos los siguientes comandos:

```git
python sobel_filter.py  
```

Esta va a generar una nueva imagen que se va a guardar en la carpeta ```outputs```.

* * *

**Parte 2:**

- Desarrolle este proceso de manera distribuida donde se debe partir la imagen en n pedazos, y asignar la tarea de aplicar la máscara a N procesos distribuidos. Después deberá unificar los resultados.

* * *

#### **Resolucion - Parte 2**

Nosotros lo resolvimos a tráves del ```sobel_distribuido.py```: Este código divide una imagen en porciones, procesa cada porción en paralelo utilizando el operador de Sobel y luego recombina los resultados para crear una imagen de la imagen de entrada. El uso de multiprocessing permite acelerar el procesamiento en máquinas con múltiples núcleos de CPU.

```git
python sobel_distribuido.py  
```

Esta va a generar nuevas imagenes con algunos ejemplos de procesos en ```outputs```.

* * *

A partir de ambas implementaciones, comente los resultados de performance dependiendo de la cantidad de nodos y tamaño de imagen.

El rendimiento de las implementaciones centralizada y distribuida va a depender del **tamaño de la imagen**, ya qué a medida que el tamaño de la imagen aumenta, la cantidad de trabajo por realizar se incrementa, y la implementación distribuida puede empezar a mostrar una mejora en el tiempo de procesamiento al dividir la carga entre múltiples núcleos.

También el **número de nodos** puede afectar. Con pocos nodos, la implementación distribuida podría ser ligeramente más lenta o similar a la centralizada por la sobrecarga de la gestión de procesos y la comunicación. Si el número de nodos es óptimo tiempo de procesamiento se minimiza. Y se utiliza un número de nodos significativamente mayor que la cantidad de núcleos de CPU, la sobrecarga entre procesos puede empezar a degradar el rendimiento, haciendo que el tiempo de procesamiento aumente nuevamente.

La implementación centralizada va ser más rápida de procesar imagenes pequeñas o va a tener un rendimiento similar a la distribuida con pocos nodos, debido a la menor sobrecarga.
A medida que el tamaño de la imagen aumenta, la implementación distribuida va empezar a superar en rendimiento a la centralizada, especialmente a medida que se incrementa el número de nodos.
Por lo que la implementación distribuida debería mostrar una mejor escalabilidad con el aumento del tamaño de la imagen y el número de núcleos disponibles.

* * *

**Parte 3:**

- Mejore la aplicación del punto anterior para que, en caso de que un proceso distribuido (al que se le asignó parte de la imagen a procesar - WORKER) se caiga y no responda, el proceso principal detecte esta situación y pida este cálculo a otro proceso.

* * *

#### **Resolucion - Parte 3**

El código de ```main.py``` implementa una versión paralela del algoritmo de Sobel que distribuye el procesamiento de la imagen en múltiples procesos y reintenta automáticamente el procesamiento de las porciones que fallan, mejorando la robustez y el rendimiento del procesamiento de imágenes.

* * *

### HIT 2

**Sobel con offloading en la nube** para construir una base elástica (elástica):
Mismo objetivo de calcular sobel, pero ahora vamos a usar **Terraform** para construir nodos de trabajo cuando se requiera procesar tareas y eliminarlos al terminar. Recuerde que será necesario:

- Instalar con #user_data las herramientas necesarias (java, docker, tools, docker).
- Copiar ejecutable (jar, py, etc) o descargar imagen Docker (hub).
- Poner a correr la aplicación e integrarse al cluster de trabajo.

El objetivo de este ejercicio es que ustedes puedan construir una arquitectura escalable (tipo 1, inicial) HÍBRIDA. Debe presentar el diagrama de arquitectura y comentar su decisión de desarrollar cada servicio y donde lo “coloca”.

* * *

#### **Resolucion - HIT 2**

Nostros planteamos una arquitectura escalable de la siguiente manera

![alt text](/images/diagrama.png)

Luego dentro de la carpeta terraform fuimos avanzando con la implementación:

- ```main.tf```: Este es el archivo principal de Terraform. Contiene la configuración de los recursos que se van a crear.
- ```outputs.tf```: Este archivo define las "salidas" de Terraform. Las salidas son valores que se muestran después de que Terraform aplica la configuración, como direcciones IP de instancias, nombres de recursos creados, etc.
- ```provider.tf```: Este archivo especifica el proveedor de la nube que se va a utilizar (por ejemplo, Google Cloud, AWS, Azure). También puede contener la configuración del proveedor, como la región y el proyecto.
- ```startup.sh```: Este es un script de shell que se ejecuta al iniciar una instancia de máquina virtual. Se utiliza para configurar la instancia, instalar software, iniciar servicios, etc.
- ```terraform.tfvars```: Este archivo se utiliza para definir los valores de las variables definidas en el archivo variables.tf. Permite personalizar la configuración de Terraform sin modificar directamente los archivos .tf.
- ```variables.tf```: Este archivo define las variables que se utilizan en los archivos .tf. Las variables permiten parametrizar la configuración de Terraform, haciéndola más reutilizable y flexible.

* * *

### **#HIT 3**

**Sobel contenerizado asincrónico y escalable (BASE DE TP FINAL):** A diferencia del clúster anterior, la idea es que construya una infraestructura basada en la nube pero ahora con un enfoque diferente.
Para ello, será necesario:

**1. Desplegar con terraform un cluster de Kubernetes (GKE).**

Este será el manejador de todos los recursos que vayamos a desplegar. Es decir, va a alojar tanto los servicios de infraestructura (rabbitMQ y Redis) como los componentes de las aplicaciones que vamos a correr (frontend, backend, split, joiner, etc). Este clúster tiene que tener la siguiente configuración mínima:

- Un nodegroup para alojar los servicios de infraestructura (rabbitmq, redis, otros)
- Un nodegroup compartido para las aplicaciones del sistema (front, back, split, joiner)
- Máquinas virtuales (fuera del cluster) que se encarguen de las tareas de procesamiento / cómputo intensivo.

![alt text](/images/dibujo.png)

* * *

### **Resolucion - HIT 3 - Punto 1**

Para esto modificamos el ```main.tf``` y definimos como iba a ser el nodepool. El archivo ```main.tf``` define la infraestructura en Google Cloud Platform (GCP) necesaria para desplegar un sistema híbrido que combina Kubernetes (GKE) con máquinas virtuales (VMs):

- `google_container_cluster.main_cluster`: Este recurso crea un cluster de Kubernetes (GKE) llamado `sobel-cluster`.
  - `location`: Se usa una región de GCP, especificada en `var.gcp_region`.
  - `remove_default_node_pool`: Se desactiva el node pool predeterminado, ya que se van a crear pools personalizados.
  - `initial_node_count`: Inicializa el clúster, pero sin node pool predeterminado real.
  - `node_config`: Provee una configuración mínima para habilitar la creación del clúster.
  - `ip_allocation_policy {}`: Habilita VPC nativa para la asignación automática de IPs.

- `google_container_node_pool.infra_nodepool`: Crea un node pool dedicado a servicios de infraestructura (por ejemplo, RabbitMQ o Redis).
  - `name`: Nombre del node pool: `infra-nodepool`.
  - `location`: Región del clúster, definida en `var.gcp_region`.
  - `cluster`: Se vincula al clúster `sobel-cluster`.
  - `node_config.machine_type`: Tipo de máquina, definido por `var.machine_type`.
  - `disk_type`: Disco SSD persistente (`pd-ssd`).
  - `disk_size_gb`: Tamaño del disco: 10 GB.
  - `tags`: Etiqueta `"infra"` para identificar estos nodos.
  - `initial_node_count`: Se inicia con 1 nodo.

- `google_container_node_pool.apps_nodepool`: Crea un node pool para desplegar los componentes de aplicación (frontend, backend, etc.).
  - `name`: Nombre del node pool: `apps-nodepool`.
  - `location`: Región del clúster, definida en `var.gcp_region`.
  - `cluster`: Se asocia al clúster `sobel-cluster`.
  - `node_config.machine_type`: Tipo de máquina, definido por `var.machine_type`.
  - `disk_type`: Disco SSD persistente (`pd-ssd`).
  - `disk_size_gb`: Tamaño del disco: 10 GB.
  - `tags`: Etiqueta `"apps"` para estos nodos.
  - `initial_node_count`: Se inicia con 1 nodo.

- `google_compute_instance.workers`: Crea 2 instancias de máquinas virtuales externas (fuera del clúster de GKE), para tareas intensivas de procesamiento (por ejemplo, el filtro Sobel distribuido).
  - `count`: Crea 2 instancias (`sobel-worker-0` y `sobel-worker-1`).
  - `name`: Nombre dinámico basado en el índice.
  - `machine_type`: Tipo de máquina definido en `var.machine_type`.
  - `zone`: Zona específica dentro de la región, definida en `var.gcp_zone`.
  - `tags`: Etiqueta `"worker"` para identificación.
  - `boot_disk.initialize_params.image`: Imagen base: `ubuntu-2204-lts`.
  - `boot_disk.initialize_params.type`: Disco SSD persistente (`pd-ssd`).
  - `boot_disk.initialize_params.size`: Tamaño del disco: 10 GB.
  - `metadata_startup_script`: Script de inicio (`startup.sh`) que se ejecuta automáticamente al crear la instancia.
  - `network_interface`:
    - `network`: Red por defecto (`default`).
    - `access_config {}`: Proporciona una IP pública para acceso externo.

Luego, los archivos de infraestructura se encuentran en la carpeta `infra` que contiene archivos de despliegue en formato YAML para servicios que se ejecutan en Kubernetes.

### Contenido

- `backend-deployment.yaml`: Despliega el servicio backend de la aplicación. Se conecta con RabbitMQ y Redis.
- `frontend-deployment.yaml`: Despliega la interfaz web que interactúa con el backend.
- `rabbitmq-deployment.yaml`: Despliega un broker RabbitMQ para la comunicación entre componentes (ej. master y workers).
- `redis-deployment.yaml`: Despliega un servicio Redis usado como base de datos en memoria o sistema de cacheo.

### Requisitos previos

- Tener acceso a un clúster de Kubernetes (GKE, Minikube, etc.).
- `kubectl` configurado para apuntar al clúster correcto.
- Tener creadas las namespaces necesarias (si se usan).
- Asegurarse de que los node pools estén corriendo.

### Cómo aplicar los despliegues

Desde esta carpeta, ejecutar:

```bash
kubectl apply -f rabbitmq-deployment.yaml
kubectl apply -f redis-deployment.yaml
kubectl apply -f backend-deployment.yaml
kubectl apply -f frontend-deployment.yaml
```

* * *

**2. Construir los pipelines de despliegue de todos los servicios.**

- Pipeline 1: El que construye el Kubernetes.
- Pipeline 1.1: El que despliega los servicios (base datos - Redis, sistema de colas - RabbitMQ)
- Pipeline 1.2-1.N: De cada aplicación desarrollada (frontend, backend, split, join)
- Pipeline 2: Despliegue de máquinas virtuales para construir a los workers. Objetivo deseable: Que estas máquinas sean “dinámicas”.

* * *

### **Resolucion - HIT 3 - Punto 2**

* * *

Este proyecto implementa un sistema distribuido con múltiples servicios desplegados en Kubernetes, complementado con workers externos desplegados en máquinas virtuales. Para facilitar su ejecución, se definen una serie de **pipelines automatizados** organizados por etapas.

#### Pipeline 1: Creación del clúster de Kubernetes (GKE)

Este pipeline construye el clúster GKE usando Terraform.

- **Ubicación**: `infra/terraform/`
- **Tecnología**: [Terraform](https://www.terraform.io/)
- **Tareas**:
  - Crear clúster Kubernetes (`google_container_cluster`)
  - Crear pools de nodos (`infra-nodepool`, `apps-nodepool`)
  - Asegurar conectividad para `kubectl`

```bash
cd infra/terraform
terraform init
terraform apply
```

#### Pipeline 1.1: Despliegue de servicios base (RabbitMQ, Redis)

Una vez creado el clúster, se aplican los servicios esenciales para la comunicación y caché.

- **Ubicación**: `infra/`
- **Tareas**:

```bash
kubectl apply -f rabbitmq-deployment.yaml
kubectl apply -f redis-deployment.yaml
```

#### Pipelines 1.2 - 1.N: Despliegue de servicios de aplicación

Cada componente desarrollado (backend, frontend, split, join) tiene su propio pipeline de despliegue.

```bash
# Build y push de imagen Docker:
docker build -t gcr.io/unlu-sdypp/backend:latest .
docker push gcr.io/unlu-sdypp/backend:latest
#  Aplicar manifiesto
kubectl apply -f backend-deployment.yaml
```

#### Pipeline 2: Despliegue de workers en máquinas virtuales

Este pipeline lanza VMs externas a Kubernetes que actúan como workers para el procesamiento intensivo (ej. Sobel).

- **Ubicación**: `infra/terraform/`
- **Tareas**:

```bash
terraform apply -target=google_compute_instance.workers
```

- Las VMs se inicializan con startup.sh:
  - Instalan dependencias
  - Conectan con RabbitMQ
  - Se registran como workers para recibir tareas
