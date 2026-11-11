# 119 - Scheduled EventBridge to Lambda

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

## Hints

**Why it matters:** Lambda packages compute as a small, event-driven unit. The code artifact, execution role and trigger are the contract to get right.

**What to do:** Complete the marked TODO in `main.tf`. Configure the function runtime, handler, role and memory for the scheduled job. Use the visible constraints as your checklist before you run the tests.

**When to use it:** Use Lambda for short-lived event handlers or glue code where managing a server would add cost and operational noise.

**How to approach it:** Open `main.tf` and work inside the single TODO region. Change one requirement at a time: add the named block, argument or reference, then run the tests. When a check fails, match its wording to the constraints and fix only the block it names.


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
python judge.py test 119 --dir workspaces/119-wire-eventbridge-lambda
```

> Hidden test details are only revealed after a submission.
