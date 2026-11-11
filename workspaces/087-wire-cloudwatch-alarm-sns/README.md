# 087 - CPU Alarm to SNS

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
python judge.py test 87 --dir workspaces/087-wire-cloudwatch-alarm-sns
```

> Hidden test details are only revealed after a submission.
