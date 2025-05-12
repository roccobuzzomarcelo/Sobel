#!/bin/bash

# Actualiza el sistema
apt-get update -y
apt-get upgrade -y

# Instala dependencias
apt-get install -y apt-transport-https ca-certificates curl software-properties-common gnupg lsb-release

# Instala Docker
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null

apt-get update -y
apt-get install -y docker-ce docker-ce-cli containerd.io

# Habilita Docker
systemctl start docker
systemctl enable docker

# Ejecuta contenedor de Redis
docker run -d --name redis --restart always -p 6379:6379 redis:latest

# Ejecuta contenedor de RabbitMQ con consola de gestión
docker run -d --name rabbitmq --restart always \
  -p 5672:5672 -p 15672:15672 \
  rabbitmq:3-management

# Fin del script
