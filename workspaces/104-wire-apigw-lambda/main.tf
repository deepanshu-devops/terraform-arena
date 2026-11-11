provider "aws" {
  region = var.aws_region
}

resource "aws_lambda_function" "this" {
  function_name = "app-fn"
  runtime       = "python3.12"
  handler       = "index.handler"
  filename      = "lambda.zip"
  memory_size   = 128
  environment {
    variables = { TABLE_NAME = "items" }
  }
}

resource "aws_apigatewayv2_api" "this" {
  name          = "app-api"
  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_integration" "this" {
  # TODO - Complete the aws_apigatewayv2_integration resource.
  # Add the arguments and nested blocks required for aws_apigatewayv2_integration.
}

resource "aws_apigatewayv2_route" "this" {
  route_key = "GET /items"
  target    = "integrations/${aws_apigatewayv2_integration.this.id}"
}

resource "aws_apigatewayv2_stage" "this" {
  name        = "$default"
  auto_deploy = true
  access_log_settings {
    destination_arn = aws_cloudwatch_log_group.this.arn
  }
}

resource "aws_lambda_permission" "this" {
  statement_id  = "allow-apigw"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.this.function_name
  principal     = "apigateway.amazonaws.com"
}
