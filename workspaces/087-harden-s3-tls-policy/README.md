# 087 - Deny S3 Requests Without TLS

**Level:** Level 3 - Real Infrastructure  
**Difficulty:** Medium  
**Points:** 90  
**Tags:** aws, s3, security, iam

## Scenario

A bucket policy must deny every request that does not use TLS (aws:SecureTransport = false).

## What to complete

- File: `main.tf`
- Task: Complete the aws_s3_bucket_policy resource
- Add the arguments and nested blocks required for aws_s3_bucket_policy.

## Constraints

- Create an aws_s3_bucket_policy.
- Deny when aws:SecureTransport is false.
- No public-read ACL.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `bucket_name` | `string` | `required` |

## Expected resources

- `aws_s3_bucket`
- `aws_s3_bucket_policy`

## Expected outputs

- (none)

## How to test

```powershell
python judge.py test 87 --dir workspaces/087-harden-s3-tls-policy
```

> Hidden test details are only revealed after a submission.
