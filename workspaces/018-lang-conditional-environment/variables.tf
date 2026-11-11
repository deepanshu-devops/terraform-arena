variable "environment" {
  description = "Input variable environment."
  type        = string
  default     = "dev"
}

variable "bucket_name" {
  description = "Input variable bucket_name."
  type        = string
  default     = "app-assets"
}

variable "aws_region" {
  description = "Input variable aws_region."
  type        = string
  default     = "us-east-1"
}
