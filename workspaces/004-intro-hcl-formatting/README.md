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

**What to do:** Complete the marked region in `main.tf`. Replace the tab and correct the indentation. Use the visible constraints as the checklist for names, values and references before you run the tests.

**When to use it:** Reach for this whenever you add a new block or argument by hand rather than copying generated code.

**How to approach it:** `main.tf` already contains the full configuration, so do not add or remove arguments. Replace tabs with two-space indentation, align each `=` within a block, and keep every closing brace aligned with its opening block. Run the tests, then fix the exact line named by the remaining formatting finding.


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
