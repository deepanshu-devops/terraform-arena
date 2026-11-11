# 109 - Scheduled EventBridge to Lambda

**Level:** Level 4 - Composition  
**Difficulty:** Hard  
**Points:** 130  
**Tags:** aws, eventbridge, lambda, automation

## Scenario

Trigger a Lambda every five minutes using an EventBridge rule and a target, with invoke permission.

## What to complete

- File: `main.tf`
- Task: Complete the scheduled function
- Configure the function runtime, handler, role and memory for the scheduled job.

## Constraints

- Create a rate(5 minutes) rule.
- Target the Lambda ARN.
- Grant lambda:InvokeFunction.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `rule_name` | `string` | `nightly-job` |
| `lambda_role_arn` | `string` | `required` |
| `lambda_runtime` | `string` | `python3.12` |
| `lambda_memory` | `number` | `128` |
| `project_name` | `string` | `terraform-practice` |
| `environment` | `string` | `dev` |
| `aws_region` | `string` | `us-east-1` |

## Expected resources

- `aws_cloudwatch_event_rule`
- `aws_cloudwatch_event_target`
- `aws_lambda_function`
- `aws_lambda_permission`

## Expected outputs

- `rule_arn`
- `lambda_arn`

## How to test

```powershell
python judge.py test 109 --dir workspaces/109-wire-eventbridge-lambda
```

> Hidden test details are only revealed after a submission.
