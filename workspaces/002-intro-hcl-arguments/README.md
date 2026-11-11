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

## Hints

**Why it matters:** HCL is the language Terraform evaluates. Small syntax mistakes here turn into confusing plan errors later, so slow, deliberate practice pays off.

**What to do:** Complete the marked TODO in `variables.tf`. Add the description, type and default arguments. Use the visible constraints as your checklist before you run the tests.

**When to use it:** Reach for this whenever you add a new block or argument by hand rather than copying generated code.

**How to approach it:** Open `variables.tf` and work inside the single TODO region. Change one requirement at a time: add the named block, argument or reference, then run the tests. When a check fails, match its wording to the constraints and fix only the block it names.


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
