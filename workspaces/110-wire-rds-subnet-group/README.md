# 110 - RDS Instance in a Subnet Group

**Level:** Level 4 - Composition  
**Difficulty:** Medium  
**Points:** 110  
**Tags:** aws, rds, database, networking

## Scenario

Place a small PostgreSQL instance in a DB subnet group and keep it private and encrypted.

## What to complete

- File: `main.tf`
- Task: Complete the aws_db_instance resource
- Add the arguments and nested blocks required for aws_db_instance.

## Hints

**Why it matters:** Managed databases carry availability, backup and network requirements. Terraform makes those choices reviewable before a database is created.

**What to do:** Complete the marked region in `main.tf`. The work is inside `resource "aws_db_instance" "this"`. Add the arguments and nested blocks required for aws_db_instance. Use the visible constraints as the checklist for names, values and references before you run the tests.

**When to use it:** Use a managed database service when you need backups, failover and patching handled by the provider rather than by an operator.

**How to approach it:** Open `main.tf` and work only inside `resource "aws_db_instance" "this"`. Use this code shape: identifier; engine; engine_version; instance_class; allocated_storage; skip_final_snapshot; db_subnet_group_name; storage_encrypted; publicly_accessible. Use the already-declared references instead of hardcoded values: `aws_db_subnet_group.this.name`. Keep the block header and braces, indent nested blocks by two spaces, and add one argument or nested block at a time. Run the tests after each small change so the first failure points at the next name to fix.


## Constraints

- Create aws_db_subnet_group from var.subnet_ids.
- Instance references the subnet group.
- storage_encrypted and not public.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `subnet_group_name` | `string` | `app-db-subnets` |
| `subnet_ids` | `list(string)` | `required` |
| `db_engine` | `string` | `postgres` |
| `db_name` | `string` | `appdb` |
| `db_username` | `string` | `appuser` |
| `db_password` | `string` | `required` |
| `project_name` | `string` | `terraform-practice` |
| `environment` | `string` | `dev` |
| `aws_region` | `string` | `us-east-1` |

## Expected resources

- `aws_db_subnet_group`
- `aws_db_instance`

## Expected outputs

- `db_endpoint`

## How to test

```powershell
python judge.py test 110 --dir workspaces/110-wire-rds-subnet-group
```

> Hidden test details are only revealed after a submission.
