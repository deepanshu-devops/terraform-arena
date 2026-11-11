# 115 - Refactor With a moved Block

**Level:** Level 5 - Modules & Capstones  
**Difficulty:** Medium  
**Points:** 75  
**Tags:** terraform, refactor, state

## Scenario

Rename a resource address without destroying it by adding a moved block.

## What to complete

- File: `main.tf`
- Task: Complete the moved block
- Declare the old and new resource addresses so Terraform preserves state.

## Constraints

- Add a moved block.
- from and to are set.
- No resource replacement.

## Input variables

| Name | Type | Default |
| --- | --- | --- |

## Expected resources

- (see constraints)

## Expected outputs

- (none)

## How to test

```powershell
python judge.py test 115 --dir workspaces/115-refactor-moved-block
```

> Hidden test details are only revealed after a submission.
