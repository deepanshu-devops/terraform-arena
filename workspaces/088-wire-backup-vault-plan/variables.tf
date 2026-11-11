variable "vault_name" {
  description = "Input variable vault_name."
  type        = string
  default     = "app-vault"
}

variable "plan_name" {
  description = "Input variable plan_name."
  type        = string
  default     = "nightly-backup"
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
