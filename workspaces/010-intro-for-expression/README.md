# 010 - For Expressions

**Level:** Level 0 - HCL Foundations  
**Difficulty:** Easy  
**Points:** 58  
**Tags:** terraform, hcl, expressions

## Scenario

For expressions transform collections without a loop block. Build a list of upper-case names and a map from each name to its upper-case form.

## What to complete

- File: `main.tf`
- Task: Transform the names
- Write list and map for expressions over var.names.

## Constraints

- Use a list for expression with upper(name).
- Use a map for expression with name => upper(name).
- Derive both from var.names.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `names` | `list(string)` | `['web', 'api']` |

## Expected resources

- (see constraints)

## Expected outputs

- (none)

## How to test

```powershell
python judge.py test 10 --dir workspaces/010-intro-for-expression
```

> Hidden test details are only revealed after a submission.
