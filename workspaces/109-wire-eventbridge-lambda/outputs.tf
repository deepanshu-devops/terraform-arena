output "rule_arn" {
  value = aws_cloudwatch_event_rule.this.arn
}

output "lambda_arn" {
  value = aws_lambda_function.this.arn
}
