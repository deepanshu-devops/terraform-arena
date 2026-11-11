variable "table_name" {
  description = "Input variable table_name."
  type        = string
  default     = "items"
}

variable "lambda_runtime" {
  description = "Input variable lambda_runtime."
  type        = string
  default     = "python3.12"
}

variable "lambda_memory" {
  description = "Input variable lambda_memory."
  type        = number
  default     = 128
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
