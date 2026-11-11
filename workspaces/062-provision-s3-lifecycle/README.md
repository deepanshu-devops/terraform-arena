# 062 - Provision S3 Lifecycle Policy

**Level:** Level 2 - First Resources  
**Difficulty:** Easy  
**Points:** 50  
**Tags:** aws, s3, provisioning

## Scenario

Your platform team needs S3 Lifecycle Policy for expiring stale objects to control storage cost. Write a reusable Terraform configuration that provisions it, drives every input through variables, applies the standard tags, and exports the operational identifiers.

## What to complete

- File: `main.tf`
- Task: Complete the aws_s3_bucket_lifecycle_configuration resource
- Add the arguments and nested blocks required for aws_s3_bucket_lifecycle_configuration.

## Constraints

- Provider: aws (region from var.aws_region).
- Create exactly one resource of type aws_s3_bucket_lifecycle_configuration.
- All configurable values must come from variables declared in variables.tf.
- No hardcoded AWS credentials.
- Code must pass terraform fmt conventions (2-space indents, trailing newline, no tabs).
- Allowed supporting resources: aws_s3_bucket.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `bucket_name` | `string` | `required` |
| `aws_region` | `string` | `us-east-1` |

## Expected resources

- `aws_s3_bucket_lifecycle_configuration`

## Expected outputs

- (none)

## How to test

```powershell
python judge.py test 62 --dir workspaces/062-provision-s3-lifecycle
```

> Hidden test details are only revealed after a submission.
