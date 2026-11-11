# 126 - Workspace-Aware Naming

**Level:** Level 5 - Modules & Capstones  
**Difficulty:** Medium  
**Points:** 75  
**Tags:** terraform, state, workspaces

## Scenario

Use terraform.workspace to build environment-specific names from one configuration.

## What to complete

- File: `main.tf`
- Task: Complete the workspace-aware locals block
- Derive the bucket name from terraform.workspace and reuse it on the bucket.

## Hints

**Why it matters:** State is Terraform's record of what it manages. A remote, locked and encrypted backend protects that record when more than one person or automation runs Terraform.

**What to do:** Complete the marked TODO in `main.tf`. Derive the bucket name from terraform.workspace and reuse it on the bucket. Use the visible constraints as your checklist before you run the tests.

**When to use it:** Use a remote backend for any shared or production configuration. Local state is fine only for short-lived experiments.

**How to approach it:** Open `main.tf` and work inside the single TODO region. Change one requirement at a time: add the named block, argument or reference, then run the tests. When a check fails, match its wording to the constraints and fix only the block it names.


## Constraints

- Reference terraform.workspace.
- Use it in a resource name or tag.
- Provision an S3 bucket.

## Input variables

| Name | Type | Default |
| --- | --- | --- |

## Expected resources

- `aws_s3_bucket`

## Expected outputs

- `bucket_id`

## How to test

```powershell
python judge.py test 126 --dir workspaces/126-state-workspaces
```

> Hidden test details are only revealed after a submission.
