output "table_arn" {
  value = aws_dynamodb_table.this.arn
}

output "lambda_arn" {
  value = aws_lambda_function.this.arn
}
