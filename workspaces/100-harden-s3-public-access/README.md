# 100 - Lock Down S3 Public Access

**Level:** Level 3 - Real Infrastructure  
**Difficulty:** Medium  
**Points:** 90  
**Tags:** aws, s3, security

## Scenario

A bucket audit flagged an S3 bucket that could be made public. Add the public access block and ensure no legacy ACL re-opens it.

## What to complete

- File: `main.tf`
- Task: Complete the aws_s3_bucket_public_access_block resource
- Add the arguments and nested blocks required for aws_s3_bucket_public_access_block.

## Hints

**Why it matters:** S3 is usually the first shared service in an AWS configuration. Bucket settings, versioning, encryption and public-access blocks are common review findings.

**What to do:** Complete the marked TODO in `main.tf`. Add the arguments and nested blocks required for aws_s3_bucket_public_access_block. Use the visible constraints as your checklist before you run the tests.

**When to use it:** Use S3 when you need durable object storage for assets, logs, backups or static content, and lock down access from the start.

**How to approach it:** Open `main.tf` and work inside the single TODO region. Change one requirement at a time: add the named block, argument or reference, then run the tests. When a check fails, match its wording to the constraints and fix only the block it names.


## Constraints

- Create aws_s3_bucket_public_access_block for var.bucket_name.
- All four public access flags must be true.
- No public-read ACL anywhere.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `bucket_name` | `string` | `required` |

## Expected resources

- `aws_s3_bucket_public_access_block`

## Expected outputs

- (none)

## How to test

```powershell
python judge.py test 100 --dir workspaces/100-harden-s3-public-access
```

> Hidden test details are only revealed after a submission.
