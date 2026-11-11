variable "asg_min" {
  description = "Input variable asg_min."
  type        = number
  default     = 1
}

variable "asg_max" {
  description = "Input variable asg_max."
  type        = number
  default     = 2
}

variable "asg_desired" {
  description = "Input variable asg_desired."
  type        = number
  default     = 1
}

variable "subnet_ids" {
  description = "Input variable subnet_ids."
  type        = list(string)
}

variable "aws_region" {
  description = "Input variable aws_region."
  type        = string
  default     = "us-east-1"
}
