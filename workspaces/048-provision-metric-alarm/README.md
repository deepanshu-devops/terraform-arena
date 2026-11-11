# 048 - Provision CloudWatch CPU Alarm

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

## Hints

**Why it matters:** Observability resources turn an invisible system into something you can alert on. Metrics, logs and alarms belong with the infrastructure they monitor.

**What to do:** Complete the marked region in `main.tf`. The work is inside `resource "aws_cloudwatch_metric_alarm" "this"`. Add the arguments and nested blocks required for aws_cloudwatch_metric_alarm. Use the visible constraints as the checklist for names, values and references before you run the tests.

**When to use it:** Add monitoring whenever a resource has a failure mode that an operator must notice quickly.

**How to approach it:** Open `main.tf` and work only inside `resource "aws_cloudwatch_metric_alarm" "this"`. Use this code shape: alarm_name; comparison_operator; evaluation_periods; metric_name; namespace; period; statistic; threshold; tags; dimensions { InstanceId }. Use the already-declared references instead of hardcoded values: `var.alarm_name`, `var.project_name`, `var.environment`, `aws_instance.this.id`. Keep the block header and braces, indent nested blocks by two spaces, and add one argument or nested block at a time. Run the tests after each small change so the first failure points at the next name to fix.


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
python judge.py test 48 --dir workspaces/048-provision-metric-alarm
```

> Hidden test details are only revealed after a submission.
