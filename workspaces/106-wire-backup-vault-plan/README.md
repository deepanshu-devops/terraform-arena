# 106 - AWS Backup Vault + Plan

**Level:** Level 4 - Composition  
**Difficulty:** Medium  
**Points:** 100  
**Tags:** aws, backup, resilience

## Scenario

Create a backup vault and a nightly backup plan that targets it.

## What to complete

- File: `main.tf`
- Task: Complete the aws_backup_plan resource
- Add the arguments and nested blocks required for aws_backup_plan.

## Hints

**Why it matters:** `aws_backup_vault` is a real building block in production configurations. The exercise isolates one decision so you can recognise the same shape when it appears inside a larger module.

**What to do:** Complete the marked TODO in `main.tf`. Add the arguments and nested blocks required for aws_backup_plan. Use the visible constraints as your checklist before you run the tests.

**When to use it:** Use this pattern when the requirement is part of a reusable configuration that another person or environment must be able to reproduce.

**How to approach it:** Open `main.tf` and work inside the single TODO region. Change one requirement at a time: add the named block, argument or reference, then run the tests. When a check fails, match its wording to the constraints and fix only the block it names.


## Constraints

- Create aws_backup_vault.
- Create aws_backup_plan with a cron rule.
- Rule targets the vault.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `vault_name` | `string` | `app-vault` |
| `plan_name` | `string` | `nightly-backup` |
| `project_name` | `string` | `terraform-practice` |
| `environment` | `string` | `dev` |
| `aws_region` | `string` | `us-east-1` |

## Expected resources

- `aws_backup_vault`
- `aws_backup_plan`

## Expected outputs

- `vault_arn`
- `plan_arn`

## How to test

```powershell
python judge.py test 106 --dir workspaces/106-wire-backup-vault-plan
```

> Hidden test details are only revealed after a submission.
