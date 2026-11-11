variable "topic_name" {
  description = "Input variable topic_name."
  type        = string
  default     = "events"
}

variable "queue_name" {
  description = "Input variable queue_name."
  type        = string
  default     = "events-queue"
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
