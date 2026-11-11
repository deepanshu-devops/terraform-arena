# 012 - Optional Values With coalesce

**Level:** Level 0 - HCL Foundations  
**Difficulty:** Easy  
**Points:** 60  
**Tags:** terraform, hcl, functions

## Scenario

Variables can default to null to represent an optional value. Use coalesce() to fall back to a friendly default when the caller does not provide a nickname.

## What to complete

- File: `main.tf`
- Task: Add the fallback value
- Use coalesce with the optional variable and a default string.

## Constraints

- Declare nickname with a null default.
- Use coalesce(var.nickname, "learner") in a local value.
- Name the local display_name.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `nickname` | `string` | `None` |

## Expected resources

- (see constraints)

## Expected outputs

- (none)

## How to test

```powershell
python judge.py test 12 --dir workspaces/012-intro-null-default
```

> Hidden test details are only revealed after a submission.
