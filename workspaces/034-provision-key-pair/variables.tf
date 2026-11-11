variable "key_name" {
  description = "Input variable key_name."
  type        = string
  default     = "app-key"
}

variable "public_key" {
  description = "Input variable public_key."
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
