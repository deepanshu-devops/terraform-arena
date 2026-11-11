# 125 - Refactor With a moved Block

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

## Hints

**Why it matters:** State is Terraform's record of what it manages. A remote, locked and encrypted backend protects that record when more than one person or automation runs Terraform.

**What to do:** Complete the marked TODO in `main.tf`. Declare the old and new resource addresses so Terraform preserves state. Use the visible constraints as your checklist before you run the tests.

**When to use it:** Use a remote backend for any shared or production configuration. Local state is fine only for short-lived experiments.

**How to approach it:** Open `main.tf` and work inside the single TODO region. Change one requirement at a time: add the named block, argument or reference, then run the tests. When a check fails, match its wording to the constraints and fix only the block it names.


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
python judge.py test 125 --dir workspaces/125-refactor-moved-block
```

> Hidden test details are only revealed after a submission.
