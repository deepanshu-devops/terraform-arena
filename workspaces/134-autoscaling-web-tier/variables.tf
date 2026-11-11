variable "vpc_id" {
  description = "VPC id for the web tier."
  type        = string
}

variable "subnet_ids" {
  description = "Subnets for the ALB and Auto Scaling group."
  type        = list(string)
}

variable "instance_type" {
  description = "Free-tier instance type."
  type        = string
  default     = "t2.micro"

  validation {
    condition     = contains(["t2.micro", "t3.micro", "t2.small", "t3.small"], var.instance_type)
    error_message = "Use a free-tier instance type."
  }
}

variable "asg_min" {
  description = "Minimum fleet size."
  type        = number
  default     = 1
}

variable "asg_max" {
  description = "Maximum fleet size."
  type        = number
  default     = 2

  validation {
    condition     = var.asg_max >= 1 && var.asg_max <= 4
    error_message = "asg_max must be between 1 and 4."
  }
}

variable "asg_desired" {
  description = "Desired fleet size."
  type        = number
  default     = 1
}

variable "health_check_path" {
  description = "Target group health check path."
  type        = string
  default     = "/"
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
