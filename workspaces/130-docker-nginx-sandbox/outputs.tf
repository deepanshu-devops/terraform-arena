output "container_id" {
  description = "Container id."
  value       = docker_container.this.id
}

output "container_name" {
  description = "Container name."
  value       = docker_container.this.name
}

output "url" {
  description = "Local URL for the published port."
  value       = "http://localhost:${var.host_port}"
}
