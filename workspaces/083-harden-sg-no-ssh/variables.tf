variable "vpc_id" {
  description = "Input variable vpc_id."
  type        = string
}

variable "security_group_name" {
  description = "Input variable security_group_name."
  type        = string
  default     = "web-sg"
}

variable "aws_region" {
  description = "Input variable aws_region."
  type        = string
  default     = "us-east-1"
}
