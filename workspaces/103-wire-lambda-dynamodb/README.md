# 103 - Lambda Reading a DynamoDB Table

**Level:** Level 4 - Composition  
**Difficulty:** Hard  
**Points:** 140  
**Tags:** aws, lambda, dynamodb, iam

## Scenario

Give a Lambda function least-privilege access to one DynamoDB table and inject the table name through its environment.

## What to complete

- File: `main.tf`
- Task: Complete the aws_lambda_function resource
- Add the arguments and nested blocks required for aws_lambda_function.

## Constraints

- Create the table and a dedicated IAM role/policy.
- Scope the policy to the table ARN.
- Lambda receives TABLE_NAME.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `table_name` | `string` | `items` |
| `lambda_runtime` | `string` | `python3.12` |
| `lambda_memory` | `number` | `128` |
| `project_name` | `string` | `terraform-practice` |
| `environment` | `string` | `dev` |
| `aws_region` | `string` | `us-east-1` |

## Expected resources

- `aws_dynamodb_table`
- `aws_iam_role`
- `aws_iam_policy`
- `aws_iam_role_policy_attachment`
- `aws_lambda_function`

## Expected outputs

- `table_arn`
- `lambda_arn`

## How to test

```powershell
python judge.py test 103 --dir workspaces/103-wire-lambda-dynamodb
```

> Hidden test details are only revealed after a submission.
