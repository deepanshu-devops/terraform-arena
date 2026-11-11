# 114 - Secure S3 Bucket Provisioning

**Level:** Level 5 - Modules & Capstones  
**Difficulty:** Easy  
**Points:** 100  
**Tags:** aws, s3, security, variables

## Scenario

A new application team needs a storage bucket. Provision an AWS S3 bucket that is secure-by-default: versioning enabled, server-side encryption at rest using AES-256, and all forms of public access blocked. The configuration must be reusable across dev / staging / prod environments without editing resource blocks, and it must never hardcode credentials.

## What to complete

- File: `main.tf`
- Task: Complete the S3 bucket resource
- Set the bucket name from the input variable and add the three standard tags.

## Constraints

- Provider: AWS (hashicorp/aws); region parameterized via var.aws_region (default us-east-1).
- No hardcoded AWS credentials anywhere in the configuration.
- bucket_name must be a variable with validation: lowercase alphanumerics + hyphens, length 3–63.
- environment must be a variable restricted to dev, staging or prod.
- The S3 bucket must carry tags: Project, Environment, ManagedBy = "terraform".
- Use the modern split-resource style; no deprecated inline arguments on aws_s3_bucket.
- All four public access block flags must be true.
- Outputs must expose bucket_id, bucket_arn and bucket_region.
- Code must pass terraform fmt conventions (2-space indents, trailing newline, no tabs).

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `bucket_name` | `string` | `None` |
| `environment` | `string` | `dev` |
| `aws_region` | `string` | `us-east-1` |
| `enable_versioning` | `bool` | `True` |
| `project_name` | `string` | `terraform-practice` |

## Expected resources

- `aws_s3_bucket`
- `aws_s3_bucket_versioning`
- `aws_s3_bucket_server_side_encryption_configuration`
- `aws_s3_bucket_public_access_block`

## Expected outputs

- `bucket_id`
- `bucket_arn`
- `bucket_region`

## How to test

```powershell
python judge.py test 114 --dir workspaces/114-secure-s3-bucket
```

> Hidden test details are only revealed after a submission.
