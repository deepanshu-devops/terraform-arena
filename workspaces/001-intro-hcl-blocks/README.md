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
