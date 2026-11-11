variable "bucket_name" {
  description = "Globally unique S3 bucket name."
  type        = string

  validation {
    condition     = length(var.bucket_name) >= 3 && length(var.bucket_name) <= 63 && can(regex("^[a-z0-9-]+$", var.bucket_name))
    error_message = "Use 3-63 lowercase letters, numbers, or hyphens."
  }
}

variable "environment" {
  description = "Deployment environment."
  type        = string
  default     = "dev"

  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging or prod."
  }
}

variable "aws_region" {
  description = "AWS region."
  type        = string
  default     = "us-east-1"
}

variable "enable_versioning" {
  description = "Enable bucket versioning."
  type        = bool
  default     = true
}

variable "project_name" {
  description = "Project name used for tags."
  type        = string
  default     = "terraform-practice"
}
