provider "aws" {
  region = var.aws_region
}

resource "aws_instance" "this" {
  ami           = "ami-0123456789abcdef0"
  instance_type = "t3.micro"
  # TODO - Complete the graded block.
  # Complete this block using the challenge requirements.
  vpc_security_group_ids = [aws_security_group.this.id]
  metadata_options {
    http_tokens = "required"
  }
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
