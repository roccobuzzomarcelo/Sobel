variable "gcp_svc_key" {
  description = "Ruta al archivo JSON de la cuenta de servicio de GCP"
  type        = string
  default     = "credentials/gcp-key.json"
}

variable "project_id" {
  description = "ID del proyecto de GCP"
  type        = string
  default     = "unlu-sdypp"
}

variable "gcp_region" {
  description = "Región donde se crearán los recursos"
  type        = string
  default = "us-central1"
}

variable "gcp_zone" {
  description = "Zona específica dentro de la región"
  type        = string
  default = "us-central1-a"
}

variable "worker_count" {
  description = "Número de instancias worker a lanzar"
  type        = number
  default     = 3
}

variable "machine_type" {
  description = "Tipo de máquina para los workers"
  type        = string
  default     = "e2-medium"
}

variable "image" {
  description = "Imagen base de las máquinas virtuales"
  type        = string
  default     = "ubuntu-2204-lts"
}
