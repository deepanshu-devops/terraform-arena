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

**What to do:** Complete the marked region in `main.tf`. The work is inside `resource "aws_efs_file_system" "this"`. Add the arguments and nested blocks required for aws_efs_file_system. Use the visible constraints as the checklist for names, values and references before you run the tests.

**When to use it:** Make security controls explicit whenever a resource exposes data, identity or network access.

**How to approach it:** Open `main.tf` and work only inside `resource "aws_efs_file_system" "this"`. Use this code shape: creation_token; encrypted. Keep the block header and braces, indent nested blocks by two spaces, and add one argument or nested block at a time. Run the tests after each small change so the first failure points at the next name to fix.


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
