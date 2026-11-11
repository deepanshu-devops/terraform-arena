variable "bucket_names" {
  description = "Map of logical name to bucket name."
  type        = map(string)
  default = {
    logs   = "arena-tutorial-logs"
    assets = "arena-tutorial-assets"
  }
}

variable "aws_region" {
  description = "Region for the demo resources."
  type        = string
  default     = "us-east-1"
}
