provider "aws" {
  region = var.aws_region
}

resource "aws_subnet" "this" {
  # TODO - Complete the aws_subnet block.
  # Use count and the subnet CIDR list so one subnet is created per entry.
}
