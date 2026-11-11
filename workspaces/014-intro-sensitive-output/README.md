# 014 - Sensitive Outputs

**Level:** Level 0 - HCL Foundations  
**Difficulty:** Easy  
**Points:** 62  
**Tags:** terraform, hcl, outputs, security

## Scenario

Outputs can carry secrets. Mark a token output sensitive so Terraform redacts it in plan and apply output while still making the value available to the caller.

## What to complete

- File: `outputs.tf`
- Task: Complete the sensitive output
- Set the value from the variable and mark the output sensitive.

## Hints

**Why it matters:** HCL is the language Terraform evaluates. Small syntax mistakes here turn into confusing plan errors later, so slow, deliberate practice pays off.

**What to do:** Complete the marked TODO in `outputs.tf`. Set the value from the variable and mark the output sensitive. Use the visible constraints as your checklist before you run the tests.

**When to use it:** Reach for this whenever you add a new block or argument by hand rather than copying generated code.

**How to approach it:** Open `outputs.tf` and work inside the single TODO region. Change one requirement at a time: add the named block, argument or reference, then run the tests. When a check fails, match its wording to the constraints and fix only the block it names.


## Constraints

- Declare an output named session_token.
- Set value to var.session_token.
- Mark the output sensitive.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `session_token` | `string` | `demo-token` |

## Expected resources

- (see constraints)

## Expected outputs

- `session_token`

## How to test

```powershell
python judge.py test 14 --dir workspaces/014-intro-sensitive-output
```

> Hidden test details are only revealed after a submission.
