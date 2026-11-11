provider "aws" {
  region = var.aws_region
}

resource "aws_s3_bucket" "this" {
  bucket = "app-assets"
}

resource "aws_s3_bucket_policy" "this" {
  # TODO - Complete the aws_s3_bucket_policy resource.
  # Add the arguments and nested blocks required for aws_s3_bucket_policy.
}
