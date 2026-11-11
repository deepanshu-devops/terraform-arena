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

**What to do:** Complete the marked region in `main.tf`. The work is inside `locals`. Use a splat for every name and index for the first IP. Use the visible constraints as the checklist for names, values and references before you run the tests.

**When to use it:** Reach for this whenever you add a new block or argument by hand rather than copying generated code.

**How to approach it:** Open `main.tf` and work only inside `locals`. Use this code shape: instance_names; primary_ip. Use the already-declared references instead of hardcoded values: `var.instances`. Keep the block header and braces, indent nested blocks by two spaces, and add one argument or nested block at a time. Run the tests after each small change so the first failure points at the next name to fix.


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
