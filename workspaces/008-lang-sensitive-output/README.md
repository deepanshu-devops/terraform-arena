# 008 - Sensitive Output

**Level:** Level 1 - Terraform Language  
**Difficulty:** Easy  
**Points:** 50  
**Tags:** terraform, outputs, security

## Scenario

Expose a connection string but mark the output as sensitive so it is redacted in plan output.

## What to complete

- File: `outputs.tf`
- Task: Mark the output as sensitive
- Add the sensitive argument to the bucket_arn output.

## Constraints

- Create an output.
- Set sensitive = true.
- Provision an S3 bucket or similar resource.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `bucket_name` | `string` | `required` |

## Expected resources

- `aws_s3_bucket`

## Expected outputs

- `bucket_arn`

## How to test

```powershell
python judge.py test 8 --dir workspaces/008-lang-sensitive-output
```

> Hidden test details are only revealed after a submission.
