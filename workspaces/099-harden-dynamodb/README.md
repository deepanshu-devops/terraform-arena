# 099 - Harden a DynamoDB Table

**Level:** Level 3 - Real Infrastructure  
**Difficulty:** Medium  
**Points:** 90  
**Tags:** aws, dynamodb, security, database

## Scenario

Enable encryption, point-in-time recovery and deletion protection on a DynamoDB table.

## What to complete

- File: `main.tf`
- Task: Complete the aws_dynamodb_table resource
- Add the arguments and nested blocks required for aws_dynamodb_table.

## Hints

**Why it matters:** DynamoDB performance and cost depend on key design. Encoding that design in Terraform makes the access pattern explicit.

**What to do:** Complete the marked region in `main.tf`. The work is inside `resource "aws_dynamodb_table" "this"`. Add the arguments and nested blocks required for aws_dynamodb_table. Use the visible constraints as the checklist for names, values and references before you run the tests.

**When to use it:** Use DynamoDB for predictable key-based access at scale, especially when operational overhead must stay low.

**How to approach it:** Open `main.tf` and work only inside `resource "aws_dynamodb_table" "this"`. Use this code shape: name; billing_mode; hash_key; deletion_protection_enabled; attribute { name; type }; server_side_encryption { enabled }; point_in_time_recovery { enabled }. Keep the block header and braces, indent nested blocks by two spaces, and add one argument or nested block at a time. Run the tests after each small change so the first failure points at the next name to fix.


## Constraints

- server_side_encryption.enabled = true.
- point_in_time_recovery.enabled = true.
- deletion_protection_enabled = true.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `table_name` | `string` | `items` |

## Expected resources

- `aws_dynamodb_table`

## Expected outputs

- `table_arn`

## How to test

```powershell
python judge.py test 99 --dir workspaces/099-harden-dynamodb
```

> Hidden test details are only revealed after a submission.
