# 085 - Secure a Secrets Manager Secret

**Level:** Level 3 - Real Infrastructure  
**Difficulty:** Medium  
**Points:** 85  
**Tags:** aws, secretsmanager, kms, security

## Scenario

Store application credentials in Secrets Manager, encrypted with a rotating customer key and no recovery window.

## What to complete

- File: `main.tf`
- Task: Complete the aws_secretsmanager_secret resource
- Add the arguments and nested blocks required for aws_secretsmanager_secret.

## Constraints

- recovery_window_in_days = 0.
- Create a KMS key with rotation.
- No hardcoded credentials.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `secret_name` | `string` | `app/credentials` |

## Expected resources

- `aws_secretsmanager_secret`
- `aws_kms_key`

## Expected outputs

- `secret_arn`

## How to test

```powershell
python judge.py test 85 --dir workspaces/085-harden-secretsmanager
```

> Hidden test details are only revealed after a submission.
