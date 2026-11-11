variable "role_name" {
  description = "Input variable role_name."
  type        = string
  default     = "app-role"
}

variable "policy_name" {
  description = "Input variable policy_name."
  type        = string
  default     = "app-policy"
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
