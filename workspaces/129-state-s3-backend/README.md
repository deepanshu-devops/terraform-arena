# 129 - Remote State in S3 + DynamoDB

**Level:** Level 5 - Modules & Capstones  
**Difficulty:** Medium  
**Points:** 90  
**Tags:** terraform, state, backend

## Scenario

Configure a remote S3 backend with state locking via DynamoDB and encryption at rest.

## What to complete

- File: `versions.tf`
- Task: Complete the S3 backend configuration
- Fill in the state bucket, key, region, DynamoDB lock table and encryption flag.

## Hints

**Why it matters:** State is Terraform's record of what it manages. A remote, locked and encrypted backend protects that record when more than one person or automation runs Terraform.

**What to do:** Complete the marked TODO in `versions.tf`. Fill in the state bucket, key, region, DynamoDB lock table and encryption flag. Use the visible constraints as your checklist before you run the tests.

**When to use it:** Use a remote backend for any shared or production configuration. Local state is fine only for short-lived experiments.

**How to approach it:** Open `versions.tf` and work inside the single TODO region. Change one requirement at a time: add the named block, argument or reference, then run the tests. When a check fails, match its wording to the constraints and fix only the block it names.


## Constraints

- backend s3.
- bucket/key/region configured.
- dynamodb_table for locking.
- encrypt = true.

## Input variables

| Name | Type | Default |
| --- | --- | --- |

## Expected resources

- (see constraints)

## Expected outputs

- (none)

## How to test

```powershell
python judge.py test 129 --dir workspaces/129-state-s3-backend
```

> Hidden test details are only revealed after a submission.
