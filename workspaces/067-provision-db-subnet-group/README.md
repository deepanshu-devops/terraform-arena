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

**What to do:** Complete the marked region in `main.tf`. The work is inside `resource "aws_db_subnet_group" "this"`. Add the arguments and nested blocks required for aws_db_subnet_group. Use the visible constraints as the checklist for names, values and references before you run the tests.

**When to use it:** Use a managed database service when you need backups, failover and patching handled by the provider rather than by an operator.

**How to approach it:** Open `main.tf` and work only inside `resource "aws_db_subnet_group" "this"`. Use this code shape: name; tags; subnet_ids. Use the already-declared references instead of hardcoded values: `var.subnet_group_name`, `var.project_name`, `var.environment`, `var.subnet_ids`. Keep the block header and braces, indent nested blocks by two spaces, and add one argument or nested block at a time. Run the tests after each small change so the first failure points at the next name to fix.


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
