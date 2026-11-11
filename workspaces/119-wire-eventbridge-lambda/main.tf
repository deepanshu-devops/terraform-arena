provider "aws" {
  region = var.aws_region
}

resource "aws_cloudwatch_event_rule" "this" {
  name                = "app-rule"
  schedule_expression = "rate(5 minutes)"
}

resource "aws_cloudwatch_event_target" "this" {
  rule  = aws_cloudwatch_event_rule.this.name
  arn   = aws_lambda_function.this.arn
  input = jsonencode({})
}

resource "aws_lambda_function" "this" {
  # TODO - Complete the scheduled function.
  # Configure the function runtime, handler, role and memory for the scheduled job.
}

resource "aws_lambda_permission" "this" {
  statement_id  = "allow-apigw"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.this.function_name
  principal     = "apigateway.amazonaws.com"
}
