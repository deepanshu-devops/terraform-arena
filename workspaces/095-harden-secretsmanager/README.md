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

**What to do:** Complete the marked region in `main.tf`. The work is inside `resource "aws_secretsmanager_secret" "this"`. Add the arguments and nested blocks required for aws_secretsmanager_secret. Use the visible constraints as the checklist for names, values and references before you run the tests.

**When to use it:** Use a secret store for credentials and API keys that applications read at runtime.

**How to approach it:** Open `main.tf` and work only inside `resource "aws_secretsmanager_secret" "this"`. Use this code shape: name; recovery_window_in_days. Keep the block header and braces, indent nested blocks by two spaces, and add one argument or nested block at a time. Run the tests after each small change so the first failure points at the next name to fix.


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
