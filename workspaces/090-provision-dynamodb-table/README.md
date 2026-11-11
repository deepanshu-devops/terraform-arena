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

**What to do:** Complete the marked TODO in `main.tf`. Add the arguments and nested blocks required for aws_dynamodb_table. Use the visible constraints as your checklist before you run the tests.

**When to use it:** Use DynamoDB for predictable key-based access at scale, especially when operational overhead must stay low.

**How to approach it:** Open `main.tf` and work inside the single TODO region. Change one requirement at a time: add the named block, argument or reference, then run the tests. When a check fails, match its wording to the constraints and fix only the block it names.


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
