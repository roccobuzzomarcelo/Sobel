# outputs.tf

output "kubernetes_cluster_name" {
  value = google_container_cluster.main_cluster.name
}

output "worker_instance_ips" {
  description = "Direcciones IP públicas de las instancias de workers"
  value       = [for instance in google_compute_instance.workers : instance.network_interface[0].access_config[0].nat_ip]
}