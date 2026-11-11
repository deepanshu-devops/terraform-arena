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

**What to do:** Complete the marked region in `main.tf`. The work is inside `moved`. Declare the old and new resource addresses so Terraform preserves state. Use the visible constraints as the checklist for names, values and references before you run the tests.

**When to use it:** Use a remote backend for any shared or production configuration. Local state is fine only for short-lived experiments.

**How to approach it:** Open `main.tf` and work only inside `moved`. Use this code shape: from; to. Use the already-declared references instead of hardcoded values: `aws_s3_bucket.old`, `aws_s3_bucket.new`. Keep the block header and braces, indent nested blocks by two spaces, and add one argument or nested block at a time. Run the tests after each small change so the first failure points at the next name to fix.


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
