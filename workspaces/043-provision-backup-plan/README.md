# 043 - Provision AWS Backup Plan

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

## Hints

**Why it matters:** `aws_backup_plan` is a real building block in production configurations. The exercise isolates one decision so you can recognise the same shape when it appears inside a larger module.

**What to do:** Complete the marked TODO in `main.tf`. Add the arguments and nested blocks required for aws_backup_plan. Use the visible constraints as your checklist before you run the tests.

**When to use it:** Use this pattern when the requirement is part of a reusable configuration that another person or environment must be able to reproduce.

**How to approach it:** Open `main.tf` and work inside the single TODO region. Change one requirement at a time: add the named block, argument or reference, then run the tests. When a check fails, match its wording to the constraints and fix only the block it names.


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
python judge.py test 43 --dir workspaces/043-provision-backup-plan
```

> Hidden test details are only revealed after a submission.
