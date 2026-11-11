provider "aws" {
  region = var.aws_region
}

resource "aws_kms_key" "this" {
  description         = "Arena managed key"
  enable_key_rotation = true
}

resource "aws_kms_alias" "this" {
  name          = "alias/arena-key"
  target_key_id = aws_kms_key.this.id
}

resource "aws_s3_bucket" "this" {
  bucket = "app-assets"
}

resource "aws_s3_bucket_server_side_encryption_configuration" "this" {
  # TODO - Complete the aws_s3_bucket_server_side_encryption_configuration resource.
  # Add the arguments and nested blocks required for aws_s3_bucket_server_side_encryption_configuration.
}
