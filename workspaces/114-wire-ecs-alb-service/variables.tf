variable "cluster_name" {
  description = "Input variable cluster_name."
  type        = string
  default     = "app-cluster"
}

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

variable "vpc_id" {
  description = "Input variable vpc_id."
  type        = string
}

variable "subnet_ids" {
  description = "Input variable subnet_ids."
  type        = list(string)
}

variable "security_group_ids" {
  description = "Input variable security_group_ids."
  type        = list(string)
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
