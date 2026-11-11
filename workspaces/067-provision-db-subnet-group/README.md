# 067 - Provision RDS Subnet Group

**Level:** Level 2 - First Resources  
**Difficulty:** Easy  
**Points:** 50  
**Tags:** aws, rds, provisioning

## Scenario

Your platform team needs RDS Subnet Group for database placement across private subnets. Write a reusable Terraform configuration that provisions it, drives every input through variables, applies the standard tags, and exports the operational identifiers.

## What to complete

- File: `main.tf`
- Task: Complete the aws_db_subnet_group resource
- Add the arguments and nested blocks required for aws_db_subnet_group.

## Hints

**Why it matters:** Managed databases carry availability, backup and network requirements. Terraform makes those choices reviewable before a database is created.

**What to do:** Complete the marked TODO in `main.tf`. Add the arguments and nested blocks required for aws_db_subnet_group. Use the visible constraints as your checklist before you run the tests.

**When to use it:** Use a managed database service when you need backups, failover and patching handled by the provider rather than by an operator.

**How to approach it:** Open `main.tf` and work inside the single TODO region. Change one requirement at a time: add the named block, argument or reference, then run the tests. When a check fails, match its wording to the constraints and fix only the block it names.


## Constraints

- Provider: aws (region from var.aws_region).
- Create exactly one resource of type aws_db_subnet_group.
- All configurable values must come from variables declared in variables.tf.
- No hardcoded AWS credentials.
- Code must pass terraform fmt conventions (2-space indents, trailing newline, no tabs).
- Tag the resource with Project, Environment and ManagedBy = "terraform".
- Expose outputs: subnet_group_name.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `subnet_group_name` | `string` | `app-db-subnets` |
| `subnet_ids` | `list(string)` | `required` |
| `environment` | `string` | `dev` |
| `project_name` | `string` | `terraform-practice` |
| `aws_region` | `string` | `us-east-1` |

## Expected resources

- `aws_db_subnet_group`

## Expected outputs

- `subnet_group_name`

## How to test

```powershell
python judge.py test 67 --dir workspaces/067-provision-db-subnet-group
```

> Hidden test details are only revealed after a submission.
