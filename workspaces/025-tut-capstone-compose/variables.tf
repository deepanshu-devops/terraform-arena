variable "project_name" {
  description = "Prefix for generated resource names."
  type        = string
  default     = "arena"
}

variable "environments" {
  description = "Environments that need storage."
  type        = list(string)
  default     = ["dev", "prod"]
}
