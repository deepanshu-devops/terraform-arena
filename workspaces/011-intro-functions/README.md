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

**What to do:** Complete the marked TODO in `main.tf`. Use lower and substr in the locals block. Use the visible constraints as your checklist before you run the tests.

**When to use it:** Reach for this whenever you add a new block or argument by hand rather than copying generated code.

**How to approach it:** Open `main.tf` and work inside the single TODO region. Change one requirement at a time: add the named block, argument or reference, then run the tests. When a check fails, match its wording to the constraints and fix only the block it names.


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
