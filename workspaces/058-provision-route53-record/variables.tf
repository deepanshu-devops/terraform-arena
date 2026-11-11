variable "zone_id" {
  description = "Input variable zone_id."
  type        = string
}

variable "record_name" {
  description = "Input variable record_name."
  type        = string
  default     = "app"
}

variable "record_value" {
  description = "Input variable record_value."
  type        = string
  default     = "203.0.113.10"
}

variable "aws_region" {
  description = "Input variable aws_region."
  type        = string
  default     = "us-east-1"
}
