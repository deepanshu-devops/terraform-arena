provider "aws" {
  region = var.aws_region
}

resource "aws_secretsmanager_secret" "this" {
  # TODO - Complete the aws_secretsmanager_secret resource.
  # Add the arguments and nested blocks required for aws_secretsmanager_secret.
}

resource "aws_kms_key" "this" {
  description         = "Arena managed key"
  enable_key_rotation = true
}
