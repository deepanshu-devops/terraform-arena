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

**What to do:** Complete the marked region in `main.tf`. The work is inside `locals`. Derive the bucket name from terraform.workspace and reuse it on the bucket. Use the visible constraints as the checklist for names, values and references before you run the tests.

**When to use it:** Use a remote backend for any shared or production configuration. Local state is fine only for short-lived experiments.

**How to approach it:** Open `main.tf` and work only inside `locals`. Use this code shape: bucket_name. Keep the block header and braces, indent nested blocks by two spaces, and add one argument or nested block at a time. Run the tests after each small change so the first failure points at the next name to fix.


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
