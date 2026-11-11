# 001 - Your First HCL Block

**Level:** Level 0 - HCL Foundations  
**Difficulty:** Easy  
**Points:** 40  
**Tags:** terraform, hcl, syntax

## Scenario

HCL is built from blocks. A block has a type (here locals), no labels, and a body of arguments. Complete the locals block so the configuration records the application name.

## What to complete

- File: `main.tf`
- Task: Complete the locals block
- Add the application name argument inside the block.

## Hints

**Why it matters:** HCL is the language Terraform evaluates. Small syntax mistakes here turn into confusing plan errors later, so slow, deliberate practice pays off.

**What to do:** Complete the marked region in `main.tf`. The work is inside `locals`. Add the application name argument inside the block. Use the visible constraints as the checklist for names, values and references before you run the tests.

**When to use it:** Reach for this whenever you add a new block or argument by hand rather than copying generated code.

**How to approach it:** Open `main.tf` and work only inside `locals`. Use this code shape: app_name. Keep the block header and braces, indent nested blocks by two spaces, and add one argument or nested block at a time. Run the tests after each small change so the first failure points at the next name to fix.


## Constraints

- Use a locals block.
- Define app_name with the value "terraform-arena".
- Keep the surrounding file valid HCL.

## Input variables

| Name | Type | Default |
| --- | --- | --- |

## Expected resources

- (see constraints)

## Expected outputs

- (none)

## How to test

```powershell
python judge.py test 1 --dir workspaces/001-intro-hcl-blocks
```

> Hidden test details are only revealed after a submission.
