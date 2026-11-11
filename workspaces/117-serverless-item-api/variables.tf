variable "table_name" {
  description = "DynamoDB table name."
  type        = string
  default     = "items"
}

variable "lambda_runtime" {
  description = "Lambda runtime."
  type        = string
  default     = "python3.12"
}

variable "lambda_memory" {
  description = "Lambda memory size in MB."
  type        = number
  default     = 128

  validation {
    condition     = var.lambda_memory >= 128 && var.lambda_memory <= 512
    error_message = "lambda_memory must be between 128 and 512 MB."
  }
}

variable "api_stage" {
  description = "HTTP API stage name."
  type        = string
  default     = "prod"
}

variable "aws_region" {
  description = "AWS region."
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Project name used for tags."
  type        = string
  default     = "terraform-practice"
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
