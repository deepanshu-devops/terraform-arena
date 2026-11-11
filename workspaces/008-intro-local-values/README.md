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

**What to do:** Complete the marked TODO in `main.tf`. Define project and derive bucket_name with an interpolation. Use the visible constraints as your checklist before you run the tests.

**When to use it:** Reach for this whenever you add a new block or argument by hand rather than copying generated code.

**How to approach it:** Open `main.tf` and work inside the single TODO region. Change one requirement at a time: add the named block, argument or reference, then run the tests. When a check fails, match its wording to the constraints and fix only the block it names.


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
