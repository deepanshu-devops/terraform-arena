output "api_endpoint" {
  description = "HTTP API endpoint."
  value       = aws_apigatewayv2_api.this.api_endpoint
}

output "lambda_name" {
  description = "Lambda function name."
  value       = aws_lambda_function.this.function_name
}

output "table_name" {
  description = "DynamoDB table name."
  value       = aws_dynamodb_table.this.name
}
