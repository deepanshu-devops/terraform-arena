# 001 - Your First HCL Block

**Level:** Level 0 - HCL Foundations  
**Difficulty:** Easy  
**Points:** 40  
**Tags:** terraform, hcl, syntax

## Scenario

HCL is built from blocks. A block has a type (here locals), no labels, and a body of arguments. Complete the locals block so the configuration records the application name.

## What to complete

- File: `main.tf`
- Task: Complete the locals block
- Add the application name argument inside the block.

## Hints

**Why it matters:** HCL is the language Terraform evaluates. Small syntax mistakes here turn into confusing plan errors later, so slow, deliberate practice pays off.

**What to do:** Complete the marked TODO in `main.tf`. Add the application name argument inside the block. Use the visible constraints as your checklist before you run the tests.

**When to use it:** Reach for this whenever you add a new block or argument by hand rather than copying generated code.

**How to approach it:** Open `main.tf` and work inside the single TODO region. Change one requirement at a time: add the named block, argument or reference, then run the tests. When a check fails, match its wording to the constraints and fix only the block it names.


## Constraints

- Use a locals block.
- Define app_name with the value "terraform-arena".
- Keep the surrounding file valid HCL.

## Input variables

| Name | Type | Default |
| --- | --- | --- |

## Expected resources

- (see constraints)

## Expected outputs

- (none)

## How to test

```powershell
python judge.py test 1 --dir workspaces/001-intro-hcl-blocks
```

> Hidden test details are only revealed after a submission.
