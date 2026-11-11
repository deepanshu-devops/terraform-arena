# 100 - RDS Instance in a Subnet Group

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
python judge.py test 100 --dir workspaces/100-wire-rds-subnet-group
```

> Hidden test details are only revealed after a submission.
