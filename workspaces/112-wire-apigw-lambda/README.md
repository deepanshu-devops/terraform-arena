# 112 - HTTP API Gateway to Lambda

**Level:** Level 4 - Composition  
**Difficulty:** Hard  
**Points:** 150  
**Tags:** aws, api-gateway, lambda, serverless

## Scenario

Expose a Lambda function through an HTTP API Gateway route with AWS_PROXY integration and a deployed stage.

## What to complete

- File: `main.tf`
- Task: Complete the aws_apigatewayv2_integration resource
- Add the arguments and nested blocks required for aws_apigatewayv2_integration.

## Constraints

- protocol_type = HTTP.
- AWS_PROXY integration to the Lambda invoke_arn.
- Route GET /items and auto-deploy the stage.
- Grant invoke permission.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `lambda_role_arn` | `string` | `required` |
| `lambda_runtime` | `string` | `python3.12` |
| `lambda_memory` | `number` | `128` |
| `api_stage` | `string` | `prod` |
| `project_name` | `string` | `terraform-practice` |
| `environment` | `string` | `dev` |
| `aws_region` | `string` | `us-east-1` |

## Expected resources

- `aws_lambda_function`
- `aws_apigatewayv2_api`
- `aws_apigatewayv2_integration`
- `aws_apigatewayv2_route`
- `aws_apigatewayv2_stage`
- `aws_lambda_permission`

## Expected outputs

- `api_endpoint`
- `lambda_arn`

## How to test

```powershell
python judge.py test 112 --dir workspaces/112-wire-apigw-lambda
```

> Hidden test details are only revealed after a submission.
