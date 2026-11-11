provider "aws" {
  region = var.aws_region
}

resource "aws_sqs_queue" "this" {
  # TODO - Complete the main queue.
  # Add the queue name, server-side encryption and redrive policy pointing at the DLQ.
}

resource "aws_sqs_queue" "dlq" {
  name = var.dlq_name
}
