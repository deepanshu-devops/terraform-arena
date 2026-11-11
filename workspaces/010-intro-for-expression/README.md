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

**What to do:** Complete the marked region in `main.tf`. The work is inside `locals`. Write list and map for expressions over var.names. Use the visible constraints as the checklist for names, values and references before you run the tests.

**When to use it:** Reach for this whenever you add a new block or argument by hand rather than copying generated code.

**How to approach it:** Open `main.tf` and work only inside `locals`. Use this code shape: upper_names; name_map. Use the already-declared references instead of hardcoded values: `var.names`. Keep the block header and braces, indent nested blocks by two spaces, and add one argument or nested block at a time. Run the tests after each small change so the first failure points at the next name to fix.


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
