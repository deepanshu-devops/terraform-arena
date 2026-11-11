# 018 - Conditional Expressions

**Level:** Level 1 - Terraform Language  
**Difficulty:** Easy  
**Points:** 55  
**Tags:** terraform, conditionals

## Scenario

Use a conditional expression to choose a bucket name suffix or retention value based on var.environment.

## What to complete

- File: `main.tf`
- Task: Complete the bucket name expression
- Use a conditional expression so production keeps the base name and other environments get a suffix.

## Constraints

- Use the ternary operator.
- Reference var.environment.
- Provision an S3 bucket.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `environment` | `string` | `dev` |
| `bucket_name` | `string` | `app-assets` |

## Expected resources

- `aws_s3_bucket`

## Expected outputs

- `bucket_id`

## How to test

```powershell
python judge.py test 18 --dir workspaces/018-lang-conditional-environment
```

> Hidden test details are only revealed after a submission.
