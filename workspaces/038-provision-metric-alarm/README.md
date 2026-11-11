# 038 - Provision CloudWatch CPU Alarm

**Level:** Level 2 - First Resources  
**Difficulty:** Easy  
**Points:** 50  
**Tags:** aws, cloudwatch, provisioning

## Scenario

Your platform team needs CloudWatch CPU Alarm for alerting when CPU stays high. Write a reusable Terraform configuration that provisions it, drives every input through variables, applies the standard tags, and exports the operational identifiers.

## What to complete

- File: `main.tf`
- Task: Complete the aws_cloudwatch_metric_alarm resource
- Add the arguments and nested blocks required for aws_cloudwatch_metric_alarm.

## Constraints

- Provider: aws (region from var.aws_region).
- Create exactly one resource of type aws_cloudwatch_metric_alarm.
- All configurable values must come from variables declared in variables.tf.
- No hardcoded AWS credentials.
- Code must pass terraform fmt conventions (2-space indents, trailing newline, no tabs).
- Tag the resource with Project, Environment and ManagedBy = "terraform".
- Expose outputs: alarm_arn.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `alarm_name` | `string` | `high-cpu` |
| `environment` | `string` | `dev` |
| `project_name` | `string` | `terraform-practice` |
| `aws_region` | `string` | `us-east-1` |

## Expected resources

- `aws_cloudwatch_metric_alarm`

## Expected outputs

- `alarm_arn`

## How to test

```powershell
python judge.py test 38 --dir workspaces/038-provision-metric-alarm
```

> Hidden test details are only revealed after a submission.
