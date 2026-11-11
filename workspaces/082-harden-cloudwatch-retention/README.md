# 082 - Set CloudWatch Log Retention

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

## Hints

**Why it matters:** Observability resources turn an invisible system into something you can alert on. Metrics, logs and alarms belong with the infrastructure they monitor.

**What to do:** Complete the marked TODO in `main.tf`. Add the arguments and nested blocks required for aws_cloudwatch_log_group. Use the visible constraints as your checklist before you run the tests.

**When to use it:** Add monitoring whenever a resource has a failure mode that an operator must notice quickly.

**How to approach it:** Open `main.tf` and work inside the single TODO region. Change one requirement at a time: add the named block, argument or reference, then run the tests. When a check fails, match its wording to the constraints and fix only the block it names.


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
python judge.py test 82 --dir workspaces/082-harden-cloudwatch-retention
```

> Hidden test details are only revealed after a submission.
