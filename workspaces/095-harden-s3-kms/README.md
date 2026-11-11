# 095 - Encrypt S3 With a Customer KMS Key

**Level:** Level 4 - Composition  
**Difficulty:** Hard  
**Points:** 120  
**Tags:** aws, s3, kms, security

## Scenario

Regulated data must use a customer-managed KMS key, not the default SSE-S3 key. Create the key and wire it into the bucket encryption.

## What to complete

- File: `main.tf`
- Task: Complete the aws_s3_bucket_server_side_encryption_configuration resource
- Add the arguments and nested blocks required for aws_s3_bucket_server_side_encryption_configuration.

## Constraints

- Create aws_kms_key with rotation enabled.
- Encryption uses aws:kms.
- Reference the KMS key from the encryption configuration.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `bucket_name` | `string` | `required` |

## Expected resources

- `aws_s3_bucket_server_side_encryption_configuration`
- `aws_kms_key`

## Expected outputs

- (none)

## How to test

```powershell
python judge.py test 95 --dir workspaces/095-harden-s3-kms
```

> Hidden test details are only revealed after a submission.
