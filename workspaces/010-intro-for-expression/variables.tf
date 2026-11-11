variable "names" {
  description = "Service names."
  type        = list(string)
  default     = ["web", "api"]
}
