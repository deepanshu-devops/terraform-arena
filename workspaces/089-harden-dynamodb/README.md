# 089 - Harden a DynamoDB Table

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
python judge.py test 89 --dir workspaces/089-harden-dynamodb
```

> Hidden test details are only revealed after a submission.
