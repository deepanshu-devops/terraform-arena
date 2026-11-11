variable "vpc_id" {
  description = "Input variable vpc_id."
  type        = string
}

variable "security_group_name" {
  description = "Input variable security_group_name."
  type        = string
  default     = "app-sg"
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
