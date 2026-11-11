# 034 - Provision AWS Backup Vault

**Level:** Level 2 - First Resources  
**Difficulty:** Easy  
**Points:** 50  
**Tags:** aws, backup, provisioning

## Scenario

Your platform team needs AWS Backup Vault for a vault for recovery points. Write a reusable Terraform configuration that provisions it, drives every input through variables, applies the standard tags, and exports the operational identifiers.

## What to complete

- File: `main.tf`
- Task: Complete the aws_backup_vault resource
- Add the arguments and nested blocks required for aws_backup_vault.

## Constraints

- Provider: aws (region from var.aws_region).
- Create exactly one resource of type aws_backup_vault.
- All configurable values must come from variables declared in variables.tf.
- No hardcoded AWS credentials.
- Code must pass terraform fmt conventions (2-space indents, trailing newline, no tabs).
- Tag the resource with Project, Environment and ManagedBy = "terraform".
- Expose outputs: vault_arn.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `vault_name` | `string` | `app-vault` |
| `environment` | `string` | `dev` |
| `project_name` | `string` | `terraform-practice` |
| `aws_region` | `string` | `us-east-1` |

## Expected resources

- `aws_backup_vault`

## Expected outputs

- `vault_arn`

## How to test

```powershell
python judge.py test 34 --dir workspaces/034-provision-backup-vault
```

> Hidden test details are only revealed after a submission.
