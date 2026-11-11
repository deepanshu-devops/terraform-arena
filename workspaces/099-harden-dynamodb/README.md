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

**What to do:** Complete the marked TODO in `main.tf`. Add the arguments and nested blocks required for aws_dynamodb_table. Use the visible constraints as your checklist before you run the tests.

**When to use it:** Use DynamoDB for predictable key-based access at scale, especially when operational overhead must stay low.

**How to approach it:** Open `main.tf` and work inside the single TODO region. Change one requirement at a time: add the named block, argument or reference, then run the tests. When a check fails, match its wording to the constraints and fix only the block it names.


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
