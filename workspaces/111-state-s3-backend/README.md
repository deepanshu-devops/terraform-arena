# 111 - Remote State in S3 + DynamoDB

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
python judge.py test 111 --dir workspaces/111-state-s3-backend
```

> Hidden test details are only revealed after a submission.
