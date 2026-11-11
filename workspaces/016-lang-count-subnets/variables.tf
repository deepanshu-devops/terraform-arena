variable "vpc_id" {
  description = "Input variable vpc_id."
  type        = string
}

variable "subnet_cidrs" {
  description = "Input variable subnet_cidrs."
  type        = list(string)
  default     = ["10.0.1.0/24", "10.0.2.0/24"]
}

variable "availability_zones" {
  description = "Input variable availability_zones."
  type        = list(string)
  default     = ["us-east-1a", "us-east-1b"]
}

variable "aws_region" {
  description = "Input variable aws_region."
  type        = string
  default     = "us-east-1"
}
