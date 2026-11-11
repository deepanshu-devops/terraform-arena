# 064 - Set CloudWatch Log Retention

**Level:** Level 3 - Real Infrastructure  
**Difficulty:** Easy  
**Points:** 55  
**Tags:** aws, cloudwatch, cost

## Scenario

Logs are retained forever and costing money. Set a 14-day retention policy.

## What to complete

- File: `main.tf`
- Task: Complete the aws_cloudwatch_log_group resource
- Add the arguments and nested blocks required for aws_cloudwatch_log_group.

## Constraints

- Create aws_cloudwatch_log_group.
- retention_in_days = 14.
- Name from var.log_group_name.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `log_group_name` | `string` | `/app/logs` |

## Expected resources

- `aws_cloudwatch_log_group`

## Expected outputs

- `log_group_arn`

## How to test

```powershell
python judge.py test 64 --dir workspaces/064-harden-cloudwatch-retention
```

> Hidden test details are only revealed after a submission.
