# 105 - CPU Alarm to SNS

**Level:** Level 4 - Composition  
**Difficulty:** Medium  
**Points:** 95  
**Tags:** aws, cloudwatch, sns, observability

## Scenario

Alert the on-call channel when average CPU exceeds 80% for one evaluation period.

## What to complete

- File: `main.tf`
- Task: Complete the aws_cloudwatch_metric_alarm resource
- Add the arguments and nested blocks required for aws_cloudwatch_metric_alarm.

## Hints

**Why it matters:** Observability resources turn an invisible system into something you can alert on. Metrics, logs and alarms belong with the infrastructure they monitor.

**What to do:** Complete the marked TODO in `main.tf`. Add the arguments and nested blocks required for aws_cloudwatch_metric_alarm. Use the visible constraints as your checklist before you run the tests.

**When to use it:** Add monitoring whenever a resource has a failure mode that an operator must notice quickly.

**How to approach it:** Open `main.tf` and work inside the single TODO region. Change one requirement at a time: add the named block, argument or reference, then run the tests. When a check fails, match its wording to the constraints and fix only the block it names.


## Constraints

- Create a metric alarm.
- threshold = 80, comparison GreaterThanThreshold.
- Alarm actions target the SNS topic.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `alarm_name` | `string` | `high-cpu` |
| `topic_name` | `string` | `alerts` |
| `project_name` | `string` | `terraform-practice` |
| `environment` | `string` | `dev` |
| `aws_region` | `string` | `us-east-1` |

## Expected resources

- `aws_cloudwatch_metric_alarm`
- `aws_sns_topic`

## Expected outputs

- `alarm_arn`

## How to test

```powershell
python judge.py test 105 --dir workspaces/105-wire-cloudwatch-alarm-sns
```

> Hidden test details are only revealed after a submission.
