# 118 - Harden an RDS Instance

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

## Hints

**Why it matters:** Managed databases carry availability, backup and network requirements. Terraform makes those choices reviewable before a database is created.

**What to do:** Complete the marked region in `main.tf`. The work is inside `resource "aws_db_instance" "this"`. Add the arguments and nested blocks required for aws_db_instance. Use the visible constraints as the checklist for names, values and references before you run the tests.

**When to use it:** Use a managed database service when you need backups, failover and patching handled by the provider rather than by an operator.

**How to approach it:** Open `main.tf` and work only inside `resource "aws_db_instance" "this"`. Use this code shape: identifier; engine; engine_version; instance_class; allocated_storage; skip_final_snapshot; storage_encrypted; publicly_accessible; backup_retention_period; deletion_protection. Keep the block header and braces, indent nested blocks by two spaces, and add one argument or nested block at a time. Run the tests after each small change so the first failure points at the next name to fix.


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
python judge.py test 118 --dir workspaces/118-harden-rds
```

> Hidden test details are only revealed after a submission.
