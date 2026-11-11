# 121 - Lambda Reading a DynamoDB Table

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

## Hints

**Why it matters:** Lambda packages compute as a small, event-driven unit. The code artifact, execution role and trigger are the contract to get right.

**What to do:** Complete the marked region in `main.tf`. The work is inside `resource "aws_lambda_function" "this"`. Add the arguments and nested blocks required for aws_lambda_function. Use the visible constraints as the checklist for names, values and references before you run the tests.

**When to use it:** Use Lambda for short-lived event handlers or glue code where managing a server would add cost and operational noise.

**How to approach it:** Open `main.tf` and work only inside `resource "aws_lambda_function" "this"`. Use this code shape: function_name; runtime; handler; filename; memory_size; role; environment { variables }. Use the already-declared references instead of hardcoded values: `aws_iam_role.this.arn`, `aws_dynamodb_table.this.name`. Keep the block header and braces, indent nested blocks by two spaces, and add one argument or nested block at a time. Run the tests after each small change so the first failure points at the next name to fix.


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
python judge.py test 121 --dir workspaces/121-wire-lambda-dynamodb
```

> Hidden test details are only revealed after a submission.
