# 002 - Arguments and Variable Blocks

**Level:** Level 0 - HCL Foundations  
**Difficulty:** Easy  
**Points:** 45  
**Tags:** terraform, hcl, variables

## Scenario

Arguments are key/value pairs inside a block. Declare the app_name input variable with a description, a string type and a default.

## What to complete

- File: `variables.tf`
- Task: Complete the variable block
- Add the description, type and default arguments.

## Constraints

- Declare variable app_name.
- Type must be string.
- Default must be "terraform-arena".

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `app_name` | `string` | `terraform-arena` |

## Expected resources

- (see constraints)

## Expected outputs

- (none)

## How to test

```powershell
python judge.py test 2 --dir workspaces/002-intro-hcl-arguments
```

> Hidden test details are only revealed after a submission.
