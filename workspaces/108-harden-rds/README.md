# 108 - Harden an RDS Instance

**Level:** Level 4 - Composition  
**Difficulty:** Hard  
**Points:** 130  
**Tags:** aws, rds, security, database

## Scenario

A production review found an unencrypted, publicly reachable database with no backups. Harden the instance.

## What to complete

- File: `main.tf`
- Task: Complete the aws_db_instance resource
- Add the arguments and nested blocks required for aws_db_instance.

## Constraints

- storage_encrypted = true.
- publicly_accessible = false.
- backup_retention_period >= 7.
- deletion_protection = true.
- skip_final_snapshot = true.
- db.t3.micro or smaller.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `db_engine` | `string` | `postgres` |
| `db_name` | `string` | `appdb` |
| `db_username` | `string` | `appuser` |
| `db_password` | `string` | `required` |

## Expected resources

- `aws_db_instance`

## Expected outputs

- `db_endpoint`

## How to test

```powershell
python judge.py test 108 --dir workspaces/108-harden-rds
```

> Hidden test details are only revealed after a submission.
