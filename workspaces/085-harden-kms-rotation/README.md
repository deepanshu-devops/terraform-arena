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

**What to do:** Complete the marked region in `main.tf`. The work is inside `resource "aws_kms_key" "this"`. Add the arguments and nested blocks required for aws_kms_key. Use the visible constraints as the checklist for names, values and references before you run the tests.

**When to use it:** Use a customer-managed key when you need control over encryption policy, rotation or cross-account access.

**How to approach it:** Open `main.tf` and work only inside `resource "aws_kms_key" "this"`. Use this code shape: description; enable_key_rotation; deletion_window_in_days. Keep the block header and braces, indent nested blocks by two spaces, and add one argument or nested block at a time. Run the tests after each small change so the first failure points at the next name to fix.


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
