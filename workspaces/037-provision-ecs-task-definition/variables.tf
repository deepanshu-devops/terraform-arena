variable "family" {
  description = "Input variable family."
  type        = string
  default     = "app-task"
}

variable "container_image" {
  description = "Input variable container_image."
  type        = string
  default     = "nginx:alpine"
}

variable "aws_region" {
  description = "Input variable aws_region."
  type        = string
  default     = "us-east-1"
}
