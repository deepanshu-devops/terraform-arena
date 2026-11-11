variable "subnet_group_name" {
  description = "Input variable subnet_group_name."
  type        = string
  default     = "app-db-subnets"
}

variable "subnet_ids" {
  description = "Input variable subnet_ids."
  type        = list(string)
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
