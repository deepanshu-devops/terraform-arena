provider "aws" {
  region = var.aws_region
}

resource "aws_secretsmanager_secret" "this" {
  name = "app-secret"
}

resource "aws_db_instance" "this" {
  # TODO - Complete the aws_db_instance resource.
  # Add the arguments and nested blocks required for aws_db_instance.
}
