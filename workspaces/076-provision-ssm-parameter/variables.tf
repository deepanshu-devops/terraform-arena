variable "parameter_name" {
  description = "Input variable parameter_name."
  type        = string
  default     = "/app/config"
}

variable "parameter_value" {
  description = "Input variable parameter_value."
  type        = string
}

variable "environment" {
  description = "Input variable environment."
  type        = string
  default     = "dev"
}

variable "project_name" {
  description = "Input variable project_name."
  type        = string
  default     = "terraform-practice"
}

variable "aws_region" {
  description = "Input variable aws_region."
  type        = string
  default     = "us-east-1"
}
