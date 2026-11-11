# 070 - Enable S3 Default Encryption

**Level:** Level 3 - Real Infrastructure  
**Difficulty:** Medium  
**Points:** 80  
**Tags:** aws, s3, security, encryption

## Scenario

Compliance requires every object in the bucket to be encrypted at rest with AES256 by default.

## What to complete

- File: `main.tf`
- Task: Complete the aws_s3_bucket_server_side_encryption_configuration resource
- Add the arguments and nested blocks required for aws_s3_bucket_server_side_encryption_configuration.

## Constraints

- Create the server-side encryption configuration resource.
- Use AES256 (SSE-S3).
- Bucket name from var.bucket_name.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `bucket_name` | `string` | `required` |

## Expected resources

- `aws_s3_bucket_server_side_encryption_configuration`

## Expected outputs

- (none)

## How to test

```powershell
python judge.py test 70 --dir workspaces/070-harden-s3-encryption
```

> Hidden test details are only revealed after a submission.
