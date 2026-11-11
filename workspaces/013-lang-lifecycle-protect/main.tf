provider "aws" {
  region = var.aws_region
}

resource "aws_s3_bucket" "this" {
  bucket = "app-assets"
  lifecycle {
    # TODO - Complete the graded block.
    # Complete this block using the challenge requirements.
  }
}
