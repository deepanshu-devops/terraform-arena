provider "aws" {
  region = var.aws_region
}

resource "aws_s3_bucket" "this" {
  # TODO - Repeat the bucket.
  # Add the repetition count and select a name for each instance.
}
