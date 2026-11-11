# 085 - Rotating KMS Customer Key

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

## Hints

**Why it matters:** Encryption keys are a security boundary. Key policies and rotation settings determine who can protect and recover data.

**What to do:** Complete the marked TODO in `main.tf`. Add the arguments and nested blocks required for aws_kms_key. Use the visible constraints as your checklist before you run the tests.

**When to use it:** Use a customer-managed key when you need control over encryption policy, rotation or cross-account access.

**How to approach it:** Open `main.tf` and work inside the single TODO region. Change one requirement at a time: add the named block, argument or reference, then run the tests. When a check fails, match its wording to the constraints and fix only the block it names.


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
python judge.py test 85 --dir workspaces/085-harden-kms-rotation
```

> Hidden test details are only revealed after a submission.
