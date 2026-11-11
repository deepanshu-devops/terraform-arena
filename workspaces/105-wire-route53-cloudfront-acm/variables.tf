variable "domain_name" {
  description = "Input variable domain_name."
  type        = string
  default     = "example.com"
}

variable "record_name" {
  description = "Input variable record_name."
  type        = string
  default     = "app"
}

variable "project_name" {
  description = "Input variable project_name."
  type        = string
  default     = "terraform-practice"
}

variable "environment" {
  description = "Input variable environment."
  type        = string
  default     = "dev"
}

variable "aws_region" {
  description = "Input variable aws_region."
  type        = string
  default     = "us-east-1"
}
