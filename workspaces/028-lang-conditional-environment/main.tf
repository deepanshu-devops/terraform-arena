provider "aws" {
  region = var.aws_region
}

resource "aws_s3_bucket" "this" {
  # TODO - Complete the bucket name expression.
  # Use a conditional expression so production keeps the base name and other environments get a suffix.
}
