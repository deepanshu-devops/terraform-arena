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

## Hints

**Why it matters:** HCL is the language Terraform evaluates. Small syntax mistakes here turn into confusing plan errors later, so slow, deliberate practice pays off.

**What to do:** Complete the marked TODO in `main.tf`. Write list and map for expressions over var.names. Use the visible constraints as your checklist before you run the tests.

**When to use it:** Reach for this whenever you add a new block or argument by hand rather than copying generated code.

**How to approach it:** Open `main.tf` and work inside the single TODO region. Change one requirement at a time: add the named block, argument or reference, then run the tests. When a check fails, match its wording to the constraints and fix only the block it names.


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
