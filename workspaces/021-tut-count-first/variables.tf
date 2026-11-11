variable "bucket_names" {
  description = "Names for the demo buckets."
  type        = list(string)
  default     = ["arena-demo-one", "arena-demo-two"]
}

variable "aws_region" {
  description = "Region for the demo resources."
  type        = string
  default     = "us-east-1"
}
