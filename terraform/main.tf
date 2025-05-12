resource "google_container_cluster" "main_cluster" {
  name     = "sobel-cluster"
  location = var.gcp_region

  remove_default_node_pool = true
  initial_node_count       = 1

  deletion_protection = false

  node_config {
    disk_size_gb = 25
    disk_type    = "pd-ssd"
  }
  ip_allocation_policy {}
}

resource "google_container_node_pool" "infra_nodepool" {
  name     = "infra-nodepool"
  location = var.gcp_region
  cluster  = google_container_cluster.main_cluster.name

  node_config {
    machine_type = var.machine_type # 1 vCPU
    disk_type    = "pd-ssd"    
    disk_size_gb = 10
    tags         = ["infra"]
  }

  initial_node_count = 1
}

resource "google_container_node_pool" "apps_nodepool" {
  name     = "apps-nodepool"
  location = var.gcp_region
  cluster  = google_container_cluster.main_cluster.name

  node_config {
    machine_type = var.machine_type # 1 vCPU
    disk_type    = "pd-ssd"
    disk_size_gb = 10
    tags         = ["apps"]
  }

  initial_node_count = 1
}

resource "google_compute_instance" "workers" {
  count        = 2 # 2 instancias de 1 vCPU
  name         = "sobel-worker-${count.index}"
  machine_type = var.machine_type # 1 vCPU
  zone         = var.gcp_zone

  tags = ["worker"]

  boot_disk {
    initialize_params {
      image = "ubuntu-2204-lts"
      type  = "pd-ssd"
      size  = 10
    }
  }

  metadata_startup_script = file("startup.sh")

  network_interface {
    network = "default"
    access_config {}
  }
}
