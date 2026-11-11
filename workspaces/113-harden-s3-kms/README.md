# 113 - Encrypt S3 With a Customer KMS Key

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

## Hints

**Why it matters:** S3 is usually the first shared service in an AWS configuration. Bucket settings, versioning, encryption and public-access blocks are common review findings.

**What to do:** Complete the marked TODO in `main.tf`. Add the arguments and nested blocks required for aws_s3_bucket_server_side_encryption_configuration. Use the visible constraints as your checklist before you run the tests.

**When to use it:** Use S3 when you need durable object storage for assets, logs, backups or static content, and lock down access from the start.

**How to approach it:** Open `main.tf` and work inside the single TODO region. Change one requirement at a time: add the named block, argument or reference, then run the tests. When a check fails, match its wording to the constraints and fix only the block it names.


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
python judge.py test 113 --dir workspaces/113-harden-s3-kms
```

> Hidden test details are only revealed after a submission.
