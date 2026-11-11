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

## Hints

**Why it matters:** HCL is the language Terraform evaluates. Small syntax mistakes here turn into confusing plan errors later, so slow, deliberate practice pays off.

**What to do:** Complete the marked TODO in `outputs.tf`. Write a quoted string that embeds the variable. Use the visible constraints as your checklist before you run the tests.

**When to use it:** Reach for this whenever you add a new block or argument by hand rather than copying generated code.

**How to approach it:** Open `outputs.tf` and work inside the single TODO region. Change one requirement at a time: add the named block, argument or reference, then run the tests. When a check fails, match its wording to the constraints and fix only the block it names.


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
