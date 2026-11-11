# 094 - Versioning + Lifecycle Expiry

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
python judge.py test 94 --dir workspaces/094-harden-s3-versioning-lifecycle
```

> Hidden test details are only revealed after a submission.
