variable "role_name" {
  description = "Input variable role_name."
  type        = string
  default     = "app-role"
}

variable "trusted_service" {
  description = "Input variable trusted_service."
  type        = string
  default     = "lambda.amazonaws.com"
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
