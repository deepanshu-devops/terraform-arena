# 009 - Conditional Expressions

**Level:** Level 0 - HCL Foundations  
**Difficulty:** Easy  
**Points:** 57  
**Tags:** terraform, hcl, expressions

## Scenario

A conditional expression chooses one of two values: condition ? true_value : false_value. Use the environment variable to pick a production flag and a log-retention period.

## What to complete

- File: `main.tf`
- Task: Add the conditional locals
- Compare the environment and choose retention values.

## Hints

**Why it matters:** HCL is the language Terraform evaluates. Small syntax mistakes here turn into confusing plan errors later, so slow, deliberate practice pays off.

**What to do:** Complete the marked TODO in `main.tf`. Compare the environment and choose retention values. Use the visible constraints as your checklist before you run the tests.

**When to use it:** Reach for this whenever you add a new block or argument by hand rather than copying generated code.

**How to approach it:** Open `main.tf` and work inside the single TODO region. Change one requirement at a time: add the named block, argument or reference, then run the tests. When a check fails, match its wording to the constraints and fix only the block it names.


## Constraints

- Treat "prod" as production.
- Set log retention to 30 days in production and 7 otherwise.
- Derive both values in the locals block.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `environment` | `string` | `dev` |

## Expected resources

- (see constraints)

## Expected outputs

- (none)

## How to test

```powershell
python judge.py test 9 --dir workspaces/009-intro-conditional
```

> Hidden test details are only revealed after a submission.
