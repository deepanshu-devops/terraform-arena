output "api_endpoint" {
  value = aws_apigatewayv2_api.this.id
}

output "lambda_arn" {
  value = aws_lambda_function.this.arn
}
