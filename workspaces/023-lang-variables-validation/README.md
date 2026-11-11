# 023 - Variable Validation

**Level:** Level 1 - Terraform Language  
**Difficulty:** Easy  
**Points:** 60  
**Tags:** terraform, variables, validation

## Scenario

Declare bucket_name with a validation block that enforces lowercase letters, digits and hyphens, and a 3-63 length.

## What to complete

- File: `variables.tf`
- Task: Complete the validation block for bucket_name
- Add a condition and error_message that enforce the documented bucket naming rules.

## Constraints

- Use can(regex(...)) or a regex() rule.
- Enforce length 3-63.
- Use the variable for the bucket name.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `bucket_name` | `string` | `required` |

## Expected resources

- `aws_s3_bucket`

## Expected outputs

- `bucket_id`

## How to test

```powershell
python judge.py test 23 --dir workspaces/023-lang-variables-validation
```

> Hidden test details are only revealed after a submission.
