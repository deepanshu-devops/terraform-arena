variable "origin_domain_name" {
  description = "Input variable origin_domain_name."
  type        = string
  default     = "example.com"
}

variable "certificate_arn" {
  description = "Input variable certificate_arn."
  type        = string
}

variable "aws_region" {
  description = "Input variable aws_region."
  type        = string
  default     = "us-east-1"
}
