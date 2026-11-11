# 088 - Enable S3 Default Encryption

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

## Hints

**Why it matters:** S3 is usually the first shared service in an AWS configuration. Bucket settings, versioning, encryption and public-access blocks are common review findings.

**What to do:** Complete the marked region in `main.tf`. The work is inside `resource "aws_s3_bucket_server_side_encryption_configuration" "this"`. Add the arguments and nested blocks required for aws_s3_bucket_server_side_encryption_configuration. Use the visible constraints as the checklist for names, values and references before you run the tests.

**When to use it:** Use S3 when you need durable object storage for assets, logs, backups or static content, and lock down access from the start.

**How to approach it:** Open `main.tf` and work only inside `resource "aws_s3_bucket_server_side_encryption_configuration" "this"`. Use this code shape: bucket; rule { apply_server_side_encryption_by_default { sse_algorithm } }. Use the already-declared references instead of hardcoded values: `var.bucket_name`. Keep the block header and braces, indent nested blocks by two spaces, and add one argument or nested block at a time. Run the tests after each small change so the first failure points at the next name to fix.


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
python judge.py test 88 --dir workspaces/088-harden-s3-encryption
```

> Hidden test details are only revealed after a submission.
