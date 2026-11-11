variable "bucket_name" {
  description = "Input variable bucket_name."
  type        = string
  validation {
    # TODO - Complete the validation block for bucket_name.
    # Add a condition and error_message that enforce the documented bucket naming rules.
  }
}

variable "aws_region" {
  description = "Input variable aws_region."
  type        = string
  default     = "us-east-1"
}
