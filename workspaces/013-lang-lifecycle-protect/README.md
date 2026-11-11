# 013 - Protect a Bucket With prevent_destroy

**Level:** Level 1 - Terraform Language  
**Difficulty:** Easy  
**Points:** 55  
**Tags:** terraform, lifecycle, safety

## Scenario

Make sure the production bucket cannot be destroyed by an accidental terraform destroy.

## What to complete

- File: `main.tf`
- Task: Complete the lifecycle block
- Protect the bucket from accidental deletion with prevent_destroy.

## Constraints

- Add a lifecycle block.
- prevent_destroy = true.
- Provision an S3 bucket.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `bucket_name` | `string` | `required` |

## Expected resources

- `aws_s3_bucket`

## Expected outputs

- `bucket_id`

## How to test

```powershell
python judge.py test 13 --dir workspaces/013-lang-lifecycle-protect
```

> Hidden test details are only revealed after a submission.
