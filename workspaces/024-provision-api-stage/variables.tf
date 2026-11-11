variable "api_id" {
  description = "Input variable api_id."
  type        = string
}

variable "stage_name" {
  description = "Input variable stage_name."
  type        = string
  default     = "prod"
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
