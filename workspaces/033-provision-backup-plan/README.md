# 033 - Provision AWS Backup Plan

**Level:** Level 2 - First Resources  
**Difficulty:** Easy  
**Points:** 50  
**Tags:** aws, backup, provisioning

## Scenario

Your platform team needs AWS Backup Plan for a nightly backup schedule. Write a reusable Terraform configuration that provisions it, drives every input through variables, applies the standard tags, and exports the operational identifiers.

## What to complete

- File: `main.tf`
- Task: Complete the aws_backup_plan resource
- Add the arguments and nested blocks required for aws_backup_plan.

## Constraints

- Provider: aws (region from var.aws_region).
- Create exactly one resource of type aws_backup_plan.
- All configurable values must come from variables declared in variables.tf.
- No hardcoded AWS credentials.
- Code must pass terraform fmt conventions (2-space indents, trailing newline, no tabs).
- Tag the resource with Project, Environment and ManagedBy = "terraform".
- Expose outputs: plan_arn.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `plan_name` | `string` | `nightly-backup` |
| `environment` | `string` | `dev` |
| `project_name` | `string` | `terraform-practice` |
| `aws_region` | `string` | `us-east-1` |

## Expected resources

- `aws_backup_plan`

## Expected outputs

- `plan_arn`

## How to test

```powershell
python judge.py test 33 --dir workspaces/033-provision-backup-plan
```

> Hidden test details are only revealed after a submission.
