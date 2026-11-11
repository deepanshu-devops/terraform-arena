variable "lb_arn" {
  description = "Input variable lb_arn."
  type        = string
}

variable "target_group_arn" {
  description = "Input variable target_group_arn."
  type        = string
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
