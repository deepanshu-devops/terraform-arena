# 012 - Optional Values With coalesce

**Level:** Level 0 - HCL Foundations  
**Difficulty:** Easy  
**Points:** 60  
**Tags:** terraform, hcl, functions

## Scenario

Variables can default to null to represent an optional value. Use coalesce() to fall back to a friendly default when the caller does not provide a nickname.

## What to complete

- File: `main.tf`
- Task: Add the fallback value
- Use coalesce with the optional variable and a default string.

## Hints

**Why it matters:** HCL is the language Terraform evaluates. Small syntax mistakes here turn into confusing plan errors later, so slow, deliberate practice pays off.

**What to do:** Complete the marked region in `main.tf`. The work is inside `locals`. Use coalesce with the optional variable and a default string. Use the visible constraints as the checklist for names, values and references before you run the tests.

**When to use it:** Reach for this whenever you add a new block or argument by hand rather than copying generated code.

**How to approach it:** Open `main.tf` and work only inside `locals`. Use this code shape: display_name. Use the already-declared references instead of hardcoded values: `var.nickname`. Keep the block header and braces, indent nested blocks by two spaces, and add one argument or nested block at a time. Run the tests after each small change so the first failure points at the next name to fix.


## Constraints

- Declare nickname with a null default.
- Use coalesce(var.nickname, "learner") in a local value.
- Name the local display_name.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `nickname` | `string` | `None` |

## Expected resources

- (see constraints)

## Expected outputs

- (none)

## How to test

```powershell
python judge.py test 12 --dir workspaces/012-intro-null-default
```

> Hidden test details are only revealed after a submission.
