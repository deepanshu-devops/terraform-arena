# 070 - Provision S3 Bucket

**Level:** Level 2 - First Resources  
**Difficulty:** Easy  
**Points:** 50  
**Tags:** aws, s3, provisioning

## Scenario

Your platform team needs S3 Bucket for durable object storage for application assets. Write a reusable Terraform configuration that provisions it, drives every input through variables, applies the standard tags, and exports the operational identifiers.

## What to complete

- File: `main.tf`
- Task: Complete the aws_s3_bucket resource
- Add the arguments and nested blocks required for aws_s3_bucket.

## Hints

**Why it matters:** S3 is usually the first shared service in an AWS configuration. Bucket settings, versioning, encryption and public-access blocks are common review findings.

**What to do:** Complete the marked region in `main.tf`. The work is inside `resource "aws_s3_bucket" "this"`. Add the arguments and nested blocks required for aws_s3_bucket. Use the visible constraints as the checklist for names, values and references before you run the tests.

**When to use it:** Use S3 when you need durable object storage for assets, logs, backups or static content, and lock down access from the start.

**How to approach it:** Open `main.tf` and work only inside `resource "aws_s3_bucket" "this"`. Use this code shape: bucket; tags; force_destroy. Use the already-declared references instead of hardcoded values: `var.bucket_name`, `var.project_name`, `var.environment`. Keep the block header and braces, indent nested blocks by two spaces, and add one argument or nested block at a time. Run the tests after each small change so the first failure points at the next name to fix.


## Constraints

- Provider: aws (region from var.aws_region).
- Create exactly one resource of type aws_s3_bucket.
- All configurable values must come from variables declared in variables.tf.
- No hardcoded AWS credentials.
- Code must pass terraform fmt conventions (2-space indents, trailing newline, no tabs).
- Tag the resource with Project, Environment and ManagedBy = "terraform".
- Expose outputs: bucket_id, bucket_arn.
- Allowed supporting resources: aws_s3_bucket_versioning, aws_s3_bucket_public_access_block.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `bucket_name` | `string` | `required` |
| `environment` | `string` | `dev` |
| `project_name` | `string` | `terraform-practice` |
| `aws_region` | `string` | `us-east-1` |

## Expected resources

- `aws_s3_bucket`

## Expected outputs

- `bucket_id`
- `bucket_arn`

## How to test

```powershell
python judge.py test 70 --dir workspaces/070-provision-s3-bucket
```

> Hidden test details are only revealed after a submission.
