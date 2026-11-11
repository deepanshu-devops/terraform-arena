provider "aws" {
  region = var.aws_region
}

resource "aws_security_group" "this" {
  name        = "app-sg"
  description = "Application security group"
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "this" {
  # TODO - Complete the graded block.
  # Complete this block using the challenge requirements.
}

resource "aws_eip" "this" {
  domain   = "vpc"
  instance = aws_instance.this.id
}

resource "aws_eip_association" "this" {
  instance_id = aws_instance.this.id
}
