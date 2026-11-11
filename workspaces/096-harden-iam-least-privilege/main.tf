provider "aws" {
  region = var.aws_region
}

data "aws_iam_policy_document" "this" {
  statement {
    sid       = "DynamoDbReadWrite"
    effect    = "Allow"
    actions   = ["dynamodb:GetItem", "dynamodb:PutItem", "dynamodb:Query"]
    resources = ["${aws_dynamodb_table.this.arn}"]
  }
}

resource "aws_iam_policy" "this" {
  # TODO - Complete the aws_iam_policy resource.
  # Add the arguments and nested blocks required for aws_iam_policy.
}

resource "aws_dynamodb_table" "this" {
  name         = "app-table"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "id"
  attribute {
    name = "id"
    type = "S"
  }
  server_side_encryption {
    enabled = true
  }
  point_in_time_recovery {
    enabled = true
  }
}
