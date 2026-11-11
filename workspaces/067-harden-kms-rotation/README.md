# 067 - Rotating KMS Customer Key

**Level:** Level 3 - Real Infrastructure  
**Difficulty:** Easy  
**Points:** 60  
**Tags:** aws, kms, security

## Scenario

Create a customer-managed KMS key with automatic rotation and a short deletion window.

## What to complete

- File: `main.tf`
- Task: Complete the aws_kms_key resource
- Add the arguments and nested blocks required for aws_kms_key.

## Constraints

- enable_key_rotation = true.
- deletion_window_in_days = 7.

## Input variables

| Name | Type | Default |
| --- | --- | --- |

## Expected resources

- `aws_kms_key`

## Expected outputs

- `key_arn`

## How to test

```powershell
python judge.py test 67 --dir workspaces/067-harden-kms-rotation
```

> Hidden test details are only revealed after a submission.
