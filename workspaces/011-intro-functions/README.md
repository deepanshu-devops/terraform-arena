# 011 - Built-in Functions

**Level:** Level 0 - HCL Foundations  
**Difficulty:** Easy  
**Points:** 59  
**Tags:** terraform, hcl, functions

## Scenario

Terraform ships with functions for strings, collections, numbers and encoding. Normalise a bucket name with lower() and take a short prefix with substr().

## What to complete

- File: `main.tf`
- Task: Normalise the bucket name
- Use lower and substr in the locals block.

## Hints

**Why it matters:** HCL is the language Terraform evaluates. Small syntax mistakes here turn into confusing plan errors later, so slow, deliberate practice pays off.

**What to do:** Complete the marked region in `main.tf`. The work is inside `locals`. Use lower and substr in the locals block. Use the visible constraints as the checklist for names, values and references before you run the tests.

**When to use it:** Reach for this whenever you add a new block or argument by hand rather than copying generated code.

**How to approach it:** Open `main.tf` and work only inside `locals`. Use this code shape: bucket_name; short_name. Use the already-declared references instead of hardcoded values: `var.project_name`, `local.bucket_name`. Keep the block header and braces, indent nested blocks by two spaces, and add one argument or nested block at a time. Run the tests after each small change so the first failure points at the next name to fix.


## Constraints

- Use lower() to build the bucket name.
- Use substr() to derive a short name.
- Reference local.bucket_name from the short name.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `project_name` | `string` | `Terraform-Arena` |

## Expected resources

- (see constraints)

## Expected outputs

- (none)

## How to test

```powershell
python judge.py test 11 --dir workspaces/011-intro-functions
```

> Hidden test details are only revealed after a submission.
