variable "docker_host" {
  description = "Docker daemon endpoint."
  type        = string
  default     = "npipe:////./pipe/docker_engine"
}

variable "container_name" {
  description = "Container name."
  type        = string
  default     = "tf-arena-nginx"

  validation {
    condition     = can(regex("^[a-z][a-z0-9-]*$", var.container_name))
    error_message = "Use lowercase letters, numbers and hyphens."
  }
}

variable "host_port" {
  description = "Host port."
  type        = number
  default     = 8080

  validation {
    condition     = var.host_port >= 1024 && var.host_port <= 65535
    error_message = "Use a port between 1024 and 65535."
  }
}

variable "image_name" {
  description = "Container image."
  type        = string
  default     = "nginx:alpine"
}

variable "project_name" {
  description = "Project name used for labels."
  type        = string
  default     = "terraform-practice"
}

variable "environment" {
  description = "Deployment environment."
  type        = string
  default     = "dev"
}
