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
