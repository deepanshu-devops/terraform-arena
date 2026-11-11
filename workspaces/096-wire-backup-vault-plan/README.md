# 096 - AWS Backup Vault + Plan

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
python judge.py test 96 --dir workspaces/096-wire-backup-vault-plan
```

> Hidden test details are only revealed after a submission.
