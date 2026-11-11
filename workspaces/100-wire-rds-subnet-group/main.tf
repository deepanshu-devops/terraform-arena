provider "aws" {
  region = var.aws_region
}

resource "aws_db_subnet_group" "this" {
  name       = "app-db-subnets"
  subnet_ids = var.subnet_ids
}

resource "aws_db_instance" "this" {
  # TODO - Complete the aws_db_instance resource.
  # Add the arguments and nested blocks required for aws_db_instance.
}
