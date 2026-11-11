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
