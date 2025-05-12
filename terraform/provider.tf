# GCP Provider
provider "google" {
  credentials = file(var.gcp_svc_key)
  project     = var.project_id
  region      = var.gcp_region
  zone        = var.gcp_zone
}