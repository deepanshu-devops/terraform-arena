provider "aws" {
  region = var.aws_region
}

resource "aws_iam_role" "this" {
  name = "app-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect    = "Allow"
        Principal = { Service = "lambda.amazonaws.com" }
        Action    = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_policy" "this" {
  name = "app-policy"
}

resource "aws_iam_role_policy_attachment" "this" {
  # TODO - Complete the aws_iam_role_policy_attachment resource.
  # Add the arguments and nested blocks required for aws_iam_role_policy_attachment.
}
