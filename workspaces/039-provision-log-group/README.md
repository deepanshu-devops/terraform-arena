# 039 - Provision CloudWatch Log Group

**Level:** Level 2 - First Resources  
**Difficulty:** Easy  
**Points:** 50  
**Tags:** aws, cloudwatch, provisioning

## Scenario

Your platform team needs CloudWatch Log Group for centralized application logs with retention. Write a reusable Terraform configuration that provisions it, drives every input through variables, applies the standard tags, and exports the operational identifiers.

## What to complete

- File: `main.tf`
- Task: Complete the aws_cloudwatch_log_group resource
- Add the arguments and nested blocks required for aws_cloudwatch_log_group.

## Constraints

- Provider: aws (region from var.aws_region).
- Create exactly one resource of type aws_cloudwatch_log_group.
- All configurable values must come from variables declared in variables.tf.
- No hardcoded AWS credentials.
- Code must pass terraform fmt conventions (2-space indents, trailing newline, no tabs).
- Tag the resource with Project, Environment and ManagedBy = "terraform".
- Expose outputs: log_group_arn.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `log_group_name` | `string` | `/app/logs` |
| `environment` | `string` | `dev` |
| `project_name` | `string` | `terraform-practice` |
| `aws_region` | `string` | `us-east-1` |

## Expected resources

- `aws_cloudwatch_log_group`

## Expected outputs

- `log_group_arn`

## How to test

```powershell
python judge.py test 39 --dir workspaces/039-provision-log-group
```

> Hidden test details are only revealed after a submission.
