# 012 - Locals for Common Tags

**Level:** Level 1 - Terraform Language  
**Difficulty:** Easy  
**Points:** 55  
**Tags:** terraform, locals, tags

## Scenario

Use a locals block to define common_tags and reuse it across the bucket instead of repeating tag maps.

## What to complete

- File: `main.tf`
- Task: Complete the shared tags locals block
- Define local.common_tags and merge the standard tags into it.

## Constraints

- Define local.common_tags.
- Reference local.common_tags from the bucket.
- No duplicated tag literals.

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
python judge.py test 12 --dir workspaces/012-lang-locals-common-tags
```

> Hidden test details are only revealed after a submission.
