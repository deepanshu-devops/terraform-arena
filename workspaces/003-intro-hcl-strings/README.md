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

**What to do:** Complete the marked region in `outputs.tf`. The work is inside `output "greeting"`. Write a quoted string that embeds the variable. Use the visible constraints as the checklist for names, values and references before you run the tests.

**When to use it:** Reach for this whenever you add a new block or argument by hand rather than copying generated code.

**How to approach it:** Open `outputs.tf` and work only inside `output "greeting"`. Use this code shape: value. Use the already-declared references instead of hardcoded values: `var.app_name`. Keep the block header and braces, indent nested blocks by two spaces, and add one argument or nested block at a time. Run the tests after each small change so the first failure points at the next name to fix.


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
