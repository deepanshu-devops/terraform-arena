# 009 - Conditional Expressions

**Level:** Level 0 - HCL Foundations  
**Difficulty:** Easy  
**Points:** 57  
**Tags:** terraform, hcl, expressions

## Scenario

A conditional expression chooses one of two values: condition ? true_value : false_value. Use the environment variable to pick a production flag and a log-retention period.

## What to complete

- File: `main.tf`
- Task: Add the conditional locals
- Compare the environment and choose retention values.

## Constraints

- Treat "prod" as production.
- Set log retention to 30 days in production and 7 otherwise.
- Derive both values in the locals block.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `environment` | `string` | `dev` |

## Expected resources

- (see constraints)

## Expected outputs

- (none)

## How to test

```powershell
python judge.py test 9 --dir workspaces/009-intro-conditional
```

> Hidden test details are only revealed after a submission.
