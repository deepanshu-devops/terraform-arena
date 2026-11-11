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

**What to do:** Complete the marked region in `main.tf`. The work is inside `resource "aws_backup_plan" "this"`. Add the arguments and nested blocks required for aws_backup_plan. Use the visible constraints as the checklist for names, values and references before you run the tests.

**When to use it:** Use this pattern when the requirement is part of a reusable configuration that another person or environment must be able to reproduce.

**How to approach it:** Open `main.tf` and work only inside `resource "aws_backup_plan" "this"`. Use this code shape: name; rule { rule_name; target_vault_name; schedule; schedule_expression }. Use the already-declared references instead of hardcoded values: `aws_backup_vault.this.name`. Keep the block header and braces, indent nested blocks by two spaces, and add one argument or nested block at a time. Run the tests after each small change so the first failure points at the next name to fix.


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
