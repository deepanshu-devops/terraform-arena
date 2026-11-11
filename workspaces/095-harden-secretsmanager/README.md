# 095 - Secure a Secrets Manager Secret

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

## Hints

**Why it matters:** Secrets should live in a managed secret store, not in code or state. Rotation and access policy are easier to audit there.

**What to do:** Complete the marked TODO in `main.tf`. Add the arguments and nested blocks required for aws_secretsmanager_secret. Use the visible constraints as your checklist before you run the tests.

**When to use it:** Use a secret store for credentials and API keys that applications read at runtime.

**How to approach it:** Open `main.tf` and work inside the single TODO region. Change one requirement at a time: add the named block, argument or reference, then run the tests. When a check fails, match its wording to the constraints and fix only the block it names.


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
python judge.py test 95 --dir workspaces/095-harden-secretsmanager
```

> Hidden test details are only revealed after a submission.
