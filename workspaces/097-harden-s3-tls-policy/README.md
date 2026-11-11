# 097 - Deny S3 Requests Without TLS

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

## Hints

**Why it matters:** S3 is usually the first shared service in an AWS configuration. Bucket settings, versioning, encryption and public-access blocks are common review findings.

**What to do:** Complete the marked region in `main.tf`. The work is inside `resource "aws_s3_bucket_policy" "this"`. Add the arguments and nested blocks required for aws_s3_bucket_policy. Use the visible constraints as the checklist for names, values and references before you run the tests.

**When to use it:** Use S3 when you need durable object storage for assets, logs, backups or static content, and lock down access from the start.

**How to approach it:** Open `main.tf` and work only inside `resource "aws_s3_bucket_policy" "this"`. Use this code shape: bucket; policy. Use the already-declared references instead of hardcoded values: `var.bucket_name`, `aws_s3_bucket.this.arn`. Keep the block header and braces, indent nested blocks by two spaces, and add one argument or nested block at a time. Run the tests after each small change so the first failure points at the next name to fix.


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
python judge.py test 97 --dir workspaces/097-harden-s3-tls-policy
```

> Hidden test details are only revealed after a submission.
