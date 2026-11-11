variable "state_machine_name" {
  description = "Input variable state_machine_name."
  type        = string
  default     = "order-flow"
}

variable "role_arn" {
  description = "Input variable role_arn."
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
