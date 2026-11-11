# 096 - Cap Lambda Timeout and Concurrency

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

## Hints

**Why it matters:** Lambda packages compute as a small, event-driven unit. The code artifact, execution role and trigger are the contract to get right.

**What to do:** Complete the marked region in `main.tf`. The work is inside `resource "aws_lambda_function" "this"`. Add the arguments and nested blocks required for aws_lambda_function. Use the visible constraints as the checklist for names, values and references before you run the tests.

**When to use it:** Use Lambda for short-lived event handlers or glue code where managing a server would add cost and operational noise.

**How to approach it:** Open `main.tf` and work only inside `resource "aws_lambda_function" "this"`. Use this code shape: function_name; runtime; handler; filename; memory_size; timeout; reserved_concurrent_executions; environment { variables }. Keep the block header and braces, indent nested blocks by two spaces, and add one argument or nested block at a time. Run the tests after each small change so the first failure points at the next name to fix.


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
python judge.py test 96 --dir workspaces/096-harden-lambda-limits
```

> Hidden test details are only revealed after a submission.
