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

**What to do:** Complete the marked region in `main.tf`. The work is inside `resource "aws_s3_bucket_server_side_encryption_configuration" "this"`. Add the arguments and nested blocks required for aws_s3_bucket_server_side_encryption_configuration. Use the visible constraints as the checklist for names, values and references before you run the tests.

**When to use it:** Use S3 when you need durable object storage for assets, logs, backups or static content, and lock down access from the start.

**How to approach it:** Open `main.tf` and work only inside `resource "aws_s3_bucket_server_side_encryption_configuration" "this"`. Use this code shape: bucket; rule { apply_server_side_encryption_by_default { sse_algorithm; kms_master_key_id } }. Use the already-declared references instead of hardcoded values: `var.bucket_name`, `aws_kms_key.this.arn`. Keep the block header and braces, indent nested blocks by two spaces, and add one argument or nested block at a time. Run the tests after each small change so the first failure points at the next name to fix.


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
