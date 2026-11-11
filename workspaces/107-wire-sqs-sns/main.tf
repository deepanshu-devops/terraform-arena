provider "aws" {
  region = var.aws_region
}

resource "aws_sns_topic" "this" {
  name = "app-topic"
}

resource "aws_sqs_queue" "this" {
  name                    = "app-queue"
  sqs_managed_sse_enabled = true
}

resource "aws_sns_topic_subscription" "this" {
  # TODO - Complete the aws_sns_topic_subscription resource.
  # Add the arguments and nested blocks required for aws_sns_topic_subscription.
}
