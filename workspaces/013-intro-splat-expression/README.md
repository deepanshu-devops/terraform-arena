# 013 - Splat Expressions

**Level:** Level 0 - HCL Foundations  
**Difficulty:** Easy  
**Points:** 61  
**Tags:** terraform, hcl, expressions

## Scenario

Splat expressions extract one attribute from every object in a list, and index syntax reads a single object. Build a list of names and the first instance's private IP.

## What to complete

- File: `main.tf`
- Task: Extract instance attributes
- Use a splat for every name and index for the first IP.

## Hints

**Why it matters:** HCL is the language Terraform evaluates. Small syntax mistakes here turn into confusing plan errors later, so slow, deliberate practice pays off.

**What to do:** Complete the marked TODO in `main.tf`. Use a splat for every name and index for the first IP. Use the visible constraints as your checklist before you run the tests.

**When to use it:** Reach for this whenever you add a new block or argument by hand rather than copying generated code.

**How to approach it:** Open `main.tf` and work inside the single TODO region. Change one requirement at a time: add the named block, argument or reference, then run the tests. When a check fails, match its wording to the constraints and fix only the block it names.


## Constraints

- Use var.instances[*].name for the name list.
- Use var.instances[0].private_ip for the primary IP.
- Keep both values in the locals block.

## Input variables

| Name | Type | Default |
| --- | --- | --- |

## Expected resources

- (see constraints)

## Expected outputs

- (none)

## How to test

```powershell
python judge.py test 13 --dir workspaces/013-intro-splat-expression
```

> Hidden test details are only revealed after a submission.
