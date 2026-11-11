variable "vpc_id" {
  description = "Input variable vpc_id."
  type        = string
}

variable "subnets" {
  description = "Input variable subnets."
  type        = map(string)
  default     = { public-a = "10.0.1.0/24", public-b = "10.0.2.0/24" }
}

variable "aws_region" {
  description = "Input variable aws_region."
  type        = string
  default     = "us-east-1"
}
