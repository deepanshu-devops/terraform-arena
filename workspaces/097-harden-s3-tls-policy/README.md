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

**What to do:** Complete the marked TODO in `main.tf`. Add the arguments and nested blocks required for aws_s3_bucket_policy. Use the visible constraints as your checklist before you run the tests.

**When to use it:** Use S3 when you need durable object storage for assets, logs, backups or static content, and lock down access from the start.

**How to approach it:** Open `main.tf` and work inside the single TODO region. Change one requirement at a time: add the named block, argument or reference, then run the tests. When a check fails, match its wording to the constraints and fix only the block it names.


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
