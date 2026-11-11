# 009 - Compose Tags With merge()

**Level:** Level 1 - Terraform Language  
**Difficulty:** Easy  
**Points:** 55  
**Tags:** terraform, functions, tags

## Scenario

Use merge() to combine a shared tag map with resource-specific tags.

## What to complete

- File: `main.tf`
- Task: Complete the locals block
- Build local.common_tags with merge() and reuse it on the bucket.

## Constraints

- Use merge().
- Keep Project, Environment, ManagedBy in the shared map.
- Provision an S3 bucket.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `project_name` | `string` | `terraform-practice` |
| `environment` | `string` | `dev` |

## Expected resources

- `aws_s3_bucket`

## Expected outputs

- `bucket_id`

## How to test

```powershell
python judge.py test 9 --dir workspaces/009-lang-functions-merge
```

> Hidden test details are only revealed after a submission.
