# 008 - Local Values and References

**Level:** Level 0 - HCL Foundations  
**Difficulty:** Easy  
**Points:** 56  
**Tags:** terraform, hcl, locals

## Scenario

Local values name expressions so they can be reused without turning them into input variables. Declare the project name and derive a bucket name from it.

## What to complete

- File: `main.tf`
- Task: Add the local values
- Define project and derive bucket_name with an interpolation.

## Hints

**Why it matters:** HCL is the language Terraform evaluates. Small syntax mistakes here turn into confusing plan errors later, so slow, deliberate practice pays off.

**What to do:** Complete the marked region in `main.tf`. The work is inside `locals`. Define project and derive bucket_name with an interpolation. Use the visible constraints as the checklist for names, values and references before you run the tests.

**When to use it:** Reach for this whenever you add a new block or argument by hand rather than copying generated code.

**How to approach it:** Open `main.tf` and work only inside `locals`. Use this code shape: project; bucket_name. Use the already-declared references instead of hardcoded values: `local.project`. Keep the block header and braces, indent nested blocks by two spaces, and add one argument or nested block at a time. Run the tests after each small change so the first failure points at the next name to fix.


## Constraints

- Set local.project to "arena".
- Derive local.bucket_name as "${local.project}-logs".
- Use references rather than repeating the literal value.

## Input variables

| Name | Type | Default |
| --- | --- | --- |

## Expected resources

- (see constraints)

## Expected outputs

- (none)

## How to test

```powershell
python judge.py test 8 --dir workspaces/008-intro-local-values
```

> Hidden test details are only revealed after a submission.
