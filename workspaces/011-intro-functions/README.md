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
