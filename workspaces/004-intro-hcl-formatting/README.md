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

## Hints

**Why it matters:** HCL is the language Terraform evaluates. Small syntax mistakes here turn into confusing plan errors later, so slow, deliberate practice pays off.

**What to do:** Complete the marked TODO in `main.tf`. Replace the tab and correct the indentation. Use the visible constraints as your checklist before you run the tests.

**When to use it:** Reach for this whenever you add a new block or argument by hand rather than copying generated code.

**How to approach it:** Open `main.tf` and work inside the single TODO region. Change one requirement at a time: add the named block, argument or reference, then run the tests. When a check fails, match its wording to the constraints and fix only the block it names.


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
