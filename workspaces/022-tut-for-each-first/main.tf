provider "aws" {
  region = var.aws_region
}

resource "aws_s3_bucket" "this" {
  # TODO - Create named instances.
  # Iterate over the map and use the current entry value as the bucket name.
}
