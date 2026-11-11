provider "aws" {
  region = var.aws_region
}

data "aws_ami" "latest" {
  # TODO - Complete the graded block.
  # Complete this block using the challenge requirements.
}

resource "aws_instance" "this" {
  ami           = data.aws_ami.latest.id
  instance_type = var.instance_type
  metadata_options {
    http_tokens = "required"
  }
}
