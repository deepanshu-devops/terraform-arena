variable "ami_id" {
  description = "Input variable ami_id."
  type        = string
}

variable "instance_type" {
  description = "Input variable instance_type."
  type        = string
  default     = "t2.micro"
}

variable "subnet_id" {
  description = "Input variable subnet_id."
  type        = string
}

variable "vpc_id" {
  description = "Input variable vpc_id."
  type        = string
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
