# 108 - Workspace-Aware Naming

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
python judge.py test 108 --dir workspaces/108-state-workspaces
```

> Hidden test details are only revealed after a submission.
