# 003 - Strings and Interpolation

**Level:** Level 0 - HCL Foundations  
**Difficulty:** Easy  
**Points:** 45  
**Tags:** terraform, hcl, strings

## Scenario

Strings are written in double quotes. Interpolation embeds an expression inside a string. Complete the greeting output.

## What to complete

- File: `outputs.tf`
- Task: Complete the greeting output
- Write a quoted string that embeds the variable.

## Constraints

- Create output "greeting".
- The value must be "Hello, ${var.app_name}!".

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `app_name` | `string` | `terraform-arena` |

## Expected resources

- (see constraints)

## Expected outputs

- `greeting`

## How to test

```powershell
python judge.py test 3 --dir workspaces/003-intro-hcl-strings
```

> Hidden test details are only revealed after a submission.
