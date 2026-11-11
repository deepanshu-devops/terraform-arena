# 104 - Versioning + Lifecycle Expiry

**Level:** Level 3 - Real Infrastructure  
**Difficulty:** Medium  
**Points:** 100  
**Tags:** aws, s3, lifecycle, cost

## Scenario

Protect against accidental overwrites while keeping cost down: enable versioning and expire stale objects after 30 days.

## What to complete

- File: `main.tf`
- Task: Complete the aws_s3_bucket_versioning resource
- Add the arguments and nested blocks required for aws_s3_bucket_versioning.

## Hints

**Why it matters:** S3 is usually the first shared service in an AWS configuration. Bucket settings, versioning, encryption and public-access blocks are common review findings.

**What to do:** Complete the marked TODO in `main.tf`. Add the arguments and nested blocks required for aws_s3_bucket_versioning. Use the visible constraints as your checklist before you run the tests.

**When to use it:** Use S3 when you need durable object storage for assets, logs, backups or static content, and lock down access from the start.

**How to approach it:** Open `main.tf` and work inside the single TODO region. Change one requirement at a time: add the named block, argument or reference, then run the tests. When a check fails, match its wording to the constraints and fix only the block it names.


## Constraints

- aws_s3_bucket_versioning must enable versioning.
- aws_s3_bucket_lifecycle_configuration must expire objects within 30 days.
- Rule status must be Enabled.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `bucket_name` | `string` | `required` |

## Expected resources

- `aws_s3_bucket_versioning`
- `aws_s3_bucket_lifecycle_configuration`

## Expected outputs

- (none)

## How to test

```powershell
python judge.py test 104 --dir workspaces/104-harden-s3-versioning-lifecycle
```

> Hidden test details are only revealed after a submission.
