# 117 - Serverless Item API

**Level:** Level 5 - Modules & Capstones  
**Difficulty:** Hard  
**Points:** 300  
**Tags:** aws, lambda, dynamodb, api-gateway, iam

## Scenario

Ship a serverless CRUD endpoint with least-privilege IAM. Provision a DynamoDB table with encryption and point-in-time recovery, a Python Lambda that receives the table name through its environment, and an HTTP API Gateway route that proxies GET /items to the function. Cap concurrency so a runaway loop cannot burn the free tier.

## What to complete

- File: `main.tf`
- Task: Complete the Lambda function
- Wire the role, runtime, memory, handler, timeout, concurrency cap, environment and tags.

## Constraints

- Provider: AWS with region from var.aws_region.
- DynamoDB: PAY_PER_REQUEST billing, hash key id (type S), SSE enabled, PITR enabled.
- Lambda execution role must trust lambda.amazonaws.com.
- A dedicated aws_iam_policy must grant only the DynamoDB actions needed, scoped to the table ARN (no "*").
- Attach the policy to the role with aws_iam_role_policy_attachment.
- Lambda: runtime and memory from variables, handler handler.lambda_handler, timeout <= 10s, reserved_concurrent_executions between 1 and 5.
- Lambda environment must expose TABLE_NAME referencing the table.
- HTTP API Gateway (protocol_type HTTP) with AWS_PROXY integration to the Lambda invoke_arn and payload_format_version 2.0.
- Route key GET /items, stage auto_deploy = true and name from var.api_stage.
- Grant API Gateway lambda:InvokeFunction through aws_lambda_permission.
- Tag DynamoDB, Lambda and the IAM role with Project, Environment, ManagedBy = "terraform".
- Outputs: api_endpoint, lambda_name, table_name.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `table_name` | `string` | `items` |
| `lambda_runtime` | `string` | `python3.12` |
| `lambda_memory` | `number` | `128` |
| `api_stage` | `string` | `prod` |
| `aws_region` | `string` | `us-east-1` |
| `project_name` | `string` | `terraform-practice` |
| `environment` | `string` | `dev` |

## Expected resources

- `aws_dynamodb_table`
- `aws_iam_role`
- `aws_iam_policy`
- `aws_iam_role_policy_attachment`
- `aws_lambda_function`
- `aws_lambda_permission`
- `aws_apigatewayv2_api`
- `aws_apigatewayv2_integration`
- `aws_apigatewayv2_route`
- `aws_apigatewayv2_stage`

## Expected outputs

- `api_endpoint`
- `lambda_name`
- `table_name`

## How to test

```powershell
python judge.py test 117 --dir workspaces/117-serverless-item-api
```

> Hidden test details are only revealed after a submission.
