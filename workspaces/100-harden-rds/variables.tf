variable "db_engine" {
  description = "Input variable db_engine."
  type        = string
  default     = "postgres"
}

variable "db_name" {
  description = "Input variable db_name."
  type        = string
  default     = "appdb"
}

variable "db_username" {
  description = "Input variable db_username."
  type        = string
  default     = "appuser"
}

variable "db_password" {
  description = "Input variable db_password."
  type        = string
}

variable "aws_region" {
  description = "Input variable aws_region."
  type        = string
  default     = "us-east-1"
}
