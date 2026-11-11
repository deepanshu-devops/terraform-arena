variable "container_name" {
  description = "Input variable container_name."
  type        = string
  default     = "web"
}

variable "image" {
  description = "Input variable image."
  type        = string
  default     = "nginx:alpine"
}

variable "host_port" {
  description = "Input variable host_port."
  type        = number
  default     = 8080
}
