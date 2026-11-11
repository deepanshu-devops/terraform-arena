# 090 - Provision DynamoDB Table

**Level:** Level 3 - Real Infrastructure  
**Difficulty:** Medium  
**Points:** 80  
**Tags:** aws, dynamodb, provisioning

## Scenario

Your platform team needs DynamoDB Table for on-demand key-value storage. Write a reusable Terraform configuration that provisions it, drives every input through variables, applies the standard tags, and exports the operational identifiers.

## What to complete

- File: `main.tf`
- Task: Complete the aws_dynamodb_table resource
- Add the arguments and nested blocks required for aws_dynamodb_table.

## Hints

**Why it matters:** DynamoDB performance and cost depend on key design. Encoding that design in Terraform makes the access pattern explicit.

**What to do:** Complete the marked region in `main.tf`. The work is inside `resource "aws_dynamodb_table" "this"`. Add the arguments and nested blocks required for aws_dynamodb_table. Use the visible constraints as the checklist for names, values and references before you run the tests.

**When to use it:** Use DynamoDB for predictable key-based access at scale, especially when operational overhead must stay low.

**How to approach it:** Open `main.tf` and work only inside `resource "aws_dynamodb_table" "this"`. Use this code shape: name; billing_mode; hash_key; tags; attribute { name; type }; server_side_encryption { enabled }; point_in_time_recovery { enabled }. Use the already-declared references instead of hardcoded values: `var.project_name`, `var.environment`. Keep the block header and braces, indent nested blocks by two spaces, and add one argument or nested block at a time. Run the tests after each small change so the first failure points at the next name to fix.


## Constraints

- Provider: aws (region from var.aws_region).
- Create exactly one resource of type aws_dynamodb_table.
- All configurable values must come from variables declared in variables.tf.
- No hardcoded AWS credentials.
- Code must pass terraform fmt conventions (2-space indents, trailing newline, no tabs).
- Tag the resource with Project, Environment and ManagedBy = "terraform".
- Expose outputs: table_arn, table_name.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `table_name` | `string` | `items` |
| `environment` | `string` | `dev` |
| `project_name` | `string` | `terraform-practice` |
| `aws_region` | `string` | `us-east-1` |

## Expected resources

- `aws_dynamodb_table`

## Expected outputs

- `table_arn`
- `table_name`

## How to test

```powershell
python judge.py test 90 --dir workspaces/090-provision-dynamodb-table
```

> Hidden test details are only revealed after a submission.
