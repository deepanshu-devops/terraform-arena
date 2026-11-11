# 081 - Provision RDS PostgreSQL Instance

**Level:** Level 3 - Real Infrastructure  
**Difficulty:** Medium  
**Points:** 80  
**Tags:** aws, rds, provisioning

## Scenario

Your platform team needs RDS PostgreSQL Instance for a small managed relational database. Write a reusable Terraform configuration that provisions it, drives every input through variables, applies the standard tags, and exports the operational identifiers.

## What to complete

- File: `main.tf`
- Task: Complete the aws_db_instance resource
- Add the arguments and nested blocks required for aws_db_instance.

## Constraints

- Provider: aws (region from var.aws_region).
- Create exactly one resource of type aws_db_instance.
- All configurable values must come from variables declared in variables.tf.
- No hardcoded AWS credentials.
- Code must pass terraform fmt conventions (2-space indents, trailing newline, no tabs).
- Tag the resource with Project, Environment and ManagedBy = "terraform".
- Expose outputs: db_endpoint.
- Allowed supporting resources: aws_db_subnet_group.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `db_engine` | `string` | `postgres` |
| `db_name` | `string` | `appdb` |
| `db_username` | `string` | `appuser` |
| `db_password` | `string` | `required` |
| `environment` | `string` | `dev` |
| `project_name` | `string` | `terraform-practice` |
| `aws_region` | `string` | `us-east-1` |

## Expected resources

- `aws_db_instance`

## Expected outputs

- `db_endpoint`

## How to test

```powershell
python judge.py test 81 --dir workspaces/081-provision-rds-instance
```

> Hidden test details are only revealed after a submission.
