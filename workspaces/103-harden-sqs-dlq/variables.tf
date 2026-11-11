variable "queue_name" {
  description = "Input variable queue_name."
  type        = string
  default     = "jobs"
}

variable "dlq_name" {
  description = "Input variable dlq_name."
  type        = string
  default     = "jobs-dlq"
}

variable "aws_region" {
  description = "Input variable aws_region."
  type        = string
  default     = "us-east-1"
}
