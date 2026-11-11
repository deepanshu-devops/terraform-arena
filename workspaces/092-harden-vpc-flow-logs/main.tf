provider "aws" {
  region = var.aws_region
}

resource "aws_vpc" "this" {
  cidr_block = "10.0.0.0/16"
  tags = {
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "terraform"
  }
}

resource "aws_cloudwatch_log_group" "this" {
  name              = "/aws/app"
  retention_in_days = 14
}

resource "aws_flow_log" "this" {
  # TODO - Complete the aws_flow_log resource.
  # Add the arguments and nested blocks required for aws_flow_log.
}
