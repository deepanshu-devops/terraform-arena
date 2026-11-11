# 004 - Format HCL by Hand

**Level:** Level 0 - HCL Foundations  
**Difficulty:** Easy  
**Points:** 50  
**Tags:** terraform, hcl, formatting

## Scenario

Terraform style is two spaces per level, no tabs, and a final newline. The block below works but is badly formatted. Fix it, or run terraform fmt, so the formatting check passes.

## What to complete

- File: `main.tf`
- Task: Fix the formatting
- Replace the tab and correct the indentation.

## Constraints

- Use two-space indentation.
- Replace tabs with spaces.
- Keep app_name defined as terraform-arena.

## Input variables

| Name | Type | Default |
| --- | --- | --- |

## Expected resources

- (see constraints)

## Expected outputs

- (none)

## How to test

```powershell
python judge.py test 4 --dir workspaces/004-intro-hcl-formatting
```

> Hidden test details are only revealed after a submission.
