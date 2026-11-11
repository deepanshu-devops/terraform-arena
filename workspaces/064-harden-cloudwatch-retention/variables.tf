variable "log_group_name" {
  description = "Input variable log_group_name."
  type        = string
  default     = "/app/logs"
}

variable "aws_region" {
  description = "Input variable aws_region."
  type        = string
  default     = "us-east-1"
}
