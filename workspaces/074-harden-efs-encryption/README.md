# 074 - Encrypted EFS File System

**Level:** Level 3 - Real Infrastructure  
**Difficulty:** Easy  
**Points:** 60  
**Tags:** aws, efs, security, storage

## Scenario

Create a shared file system with encryption at rest enabled.

## What to complete

- File: `main.tf`
- Task: Complete the aws_efs_file_system resource
- Add the arguments and nested blocks required for aws_efs_file_system.

## Constraints

- encrypted = true.
- Provide a creation_token.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `file_system_name` | `string` | `shared-assets` |

## Expected resources

- `aws_efs_file_system`

## Expected outputs

- `file_system_id`

## How to test

```powershell
python judge.py test 74 --dir workspaces/074-harden-efs-encryption
```

> Hidden test details are only revealed after a submission.
