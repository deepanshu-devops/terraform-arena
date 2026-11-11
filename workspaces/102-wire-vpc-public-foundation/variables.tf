variable "vpc_cidr" {
  description = "Input variable vpc_cidr."
  type        = string
  default     = "10.0.0.0/16"
}

variable "subnet_cidr" {
  description = "Input variable subnet_cidr."
  type        = string
  default     = "10.0.1.0/24"
}

variable "availability_zone" {
  description = "Input variable availability_zone."
  type        = string
  default     = "us-east-1a"
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
