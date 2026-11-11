variable "ami_id" {
  description = "Input variable ami_id."
  type        = string
}

variable "instance_type" {
  description = "Input variable instance_type."
  type        = string
  default     = "t2.micro"
}

variable "aws_region" {
  description = "Input variable aws_region."
  type        = string
  default     = "us-east-1"
}
