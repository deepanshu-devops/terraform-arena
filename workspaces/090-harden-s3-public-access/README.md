# 090 - Lock Down S3 Public Access

**Level:** Level 3 - Real Infrastructure  
**Difficulty:** Medium  
**Points:** 90  
**Tags:** aws, s3, security

## Scenario

A bucket audit flagged an S3 bucket that could be made public. Add the public access block and ensure no legacy ACL re-opens it.

## What to complete

- File: `main.tf`
- Task: Complete the aws_s3_bucket_public_access_block resource
- Add the arguments and nested blocks required for aws_s3_bucket_public_access_block.

## Constraints

- Create aws_s3_bucket_public_access_block for var.bucket_name.
- All four public access flags must be true.
- No public-read ACL anywhere.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `bucket_name` | `string` | `required` |

## Expected resources

- `aws_s3_bucket_public_access_block`

## Expected outputs

- (none)

## How to test

```powershell
python judge.py test 90 --dir workspaces/090-harden-s3-public-access
```

> Hidden test details are only revealed after a submission.
