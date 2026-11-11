# 055 - Provision S3 Public Access Block

**Level:** Level 2 - First Resources  
**Difficulty:** Easy  
**Points:** 50  
**Tags:** aws, s3, provisioning

## Scenario

Your platform team needs S3 Public Access Block for preventing accidental public exposure of a bucket. Write a reusable Terraform configuration that provisions it, drives every input through variables, applies the standard tags, and exports the operational identifiers.

## What to complete

- File: `main.tf`
- Task: Complete the aws_s3_bucket_public_access_block resource
- Add the arguments and nested blocks required for aws_s3_bucket_public_access_block.

## Constraints

- Provider: aws (region from var.aws_region).
- Create exactly one resource of type aws_s3_bucket_public_access_block.
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

- `aws_s3_bucket_public_access_block`

## Expected outputs

- (none)

## How to test

```powershell
python judge.py test 55 --dir workspaces/055-provision-s3-public-access-block
```

> Hidden test details are only revealed after a submission.
