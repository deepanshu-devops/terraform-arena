# 109 - KMS Key + Alias + S3 Encryption

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

## Hints

**Why it matters:** Encryption keys are a security boundary. Key policies and rotation settings determine who can protect and recover data.

**What to do:** Complete the marked region in `main.tf`. The work is inside `resource "aws_s3_bucket_server_side_encryption_configuration" "this"`. Add the arguments and nested blocks required for aws_s3_bucket_server_side_encryption_configuration. Use the visible constraints as the checklist for names, values and references before you run the tests.

**When to use it:** Use a customer-managed key when you need control over encryption policy, rotation or cross-account access.

**How to approach it:** Open `main.tf` and work only inside `resource "aws_s3_bucket_server_side_encryption_configuration" "this"`. Use this code shape: bucket; rule { apply_server_side_encryption_by_default { sse_algorithm; kms_master_key_id } }. Use the already-declared references instead of hardcoded values: `var.bucket_name`, `aws_kms_key.this.arn`. Keep the block header and braces, indent nested blocks by two spaces, and add one argument or nested block at a time. Run the tests after each small change so the first failure points at the next name to fix.


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
python judge.py test 109 --dir workspaces/109-wire-kms-s3
```

> Hidden test details are only revealed after a submission.
