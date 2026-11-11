provider "aws" {
  region = var.aws_region
}

resource "aws_s3_bucket_versioning" "this" {
  # TODO - Complete the aws_s3_bucket_versioning resource.
  # Add the arguments and nested blocks required for aws_s3_bucket_versioning.
}

resource "aws_s3_bucket_lifecycle_configuration" "this" {
  bucket = var.bucket_name
  rule {
    status = "Enabled"
    expiration {
      days = 30
    }
  }
}
