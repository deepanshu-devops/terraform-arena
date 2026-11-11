# 084 - Encrypted EFS File System

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

## Hints

**Why it matters:** Security settings are easiest to review when they are explicit in code. A default that looks harmless in a console can become a production finding.

**What to do:** Complete the marked TODO in `main.tf`. Add the arguments and nested blocks required for aws_efs_file_system. Use the visible constraints as your checklist before you run the tests.

**When to use it:** Make security controls explicit whenever a resource exposes data, identity or network access.

**How to approach it:** Open `main.tf` and work inside the single TODO region. Change one requirement at a time: add the named block, argument or reference, then run the tests. When a check fails, match its wording to the constraints and fix only the block it names.


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
python judge.py test 84 --dir workspaces/084-harden-efs-encryption
```

> Hidden test details are only revealed after a submission.
