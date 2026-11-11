# 078 - Cap Lambda Timeout and Concurrency

**Level:** Level 3 - Real Infrastructure  
**Difficulty:** Medium  
**Points:** 90  
**Tags:** aws, lambda, security, cost

## Scenario

A runaway function burned through the free tier. Cap timeout and concurrency, and remove wildcard IAM.

## What to complete

- File: `main.tf`
- Task: Complete the aws_lambda_function resource
- Add the arguments and nested blocks required for aws_lambda_function.

## Constraints

- timeout <= 10 seconds.
- reserved_concurrent_executions between 1 and 5.
- No wildcard IAM actions.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `lambda_role_arn` | `string` | `required` |
| `lambda_runtime` | `string` | `python3.12` |
| `lambda_memory` | `number` | `128` |

## Expected resources

- `aws_lambda_function`

## Expected outputs

- `lambda_arn`

## How to test

```powershell
python judge.py test 78 --dir workspaces/078-harden-lambda-limits
```

> Hidden test details are only revealed after a submission.
