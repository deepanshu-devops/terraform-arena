provider "aws" {
  region = var.aws_region
}

locals {
  # TODO - Complete the graded block.
  # Complete this block using the challenge requirements.
}

resource "aws_s3_bucket" "this" {
  bucket = "app-assets"
  tags   = local.common_tags
}
