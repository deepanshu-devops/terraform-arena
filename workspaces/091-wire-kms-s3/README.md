# 091 - KMS Key + Alias + S3 Encryption

**Level:** Level 4 - Composition  
**Difficulty:** Medium  
**Points:** 110  
**Tags:** aws, kms, s3, security

## Scenario

Create a customer KMS key with an alias and use it to encrypt an S3 bucket.

## What to complete

- File: `main.tf`
- Task: Complete the aws_s3_bucket_server_side_encryption_configuration resource
- Add the arguments and nested blocks required for aws_s3_bucket_server_side_encryption_configuration.

## Constraints

- Create key + alias.
- Bucket encryption uses aws:kms.
- Wire kms_master_key_id to the key.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `bucket_name` | `string` | `required` |
| `project_name` | `string` | `terraform-practice` |
| `environment` | `string` | `dev` |
| `aws_region` | `string` | `us-east-1` |

## Expected resources

- `aws_kms_key`
- `aws_kms_alias`
- `aws_s3_bucket`
- `aws_s3_bucket_server_side_encryption_configuration`

## Expected outputs

- `key_arn`
- `bucket_id`

## How to test

```powershell
python judge.py test 91 --dir workspaces/091-wire-kms-s3
```

> Hidden test details are only revealed after a submission.
