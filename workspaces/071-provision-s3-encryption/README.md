# 071 - Provision S3 Encryption Configuration

**Level:** Level 2 - First Resources  
**Difficulty:** Easy  
**Points:** 50  
**Tags:** aws, s3, provisioning

## Scenario

Your platform team needs S3 Encryption Configuration for encrypting objects at rest with AES256. Write a reusable Terraform configuration that provisions it, drives every input through variables, applies the standard tags, and exports the operational identifiers.

## What to complete

- File: `main.tf`
- Task: Complete the aws_s3_bucket_server_side_encryption_configuration resource
- Add the arguments and nested blocks required for aws_s3_bucket_server_side_encryption_configuration.

## Hints

**Why it matters:** S3 is usually the first shared service in an AWS configuration. Bucket settings, versioning, encryption and public-access blocks are common review findings.

**What to do:** Complete the marked region in `main.tf`. The work is inside `resource "aws_s3_bucket_server_side_encryption_configuration" "this"`. Add the arguments and nested blocks required for aws_s3_bucket_server_side_encryption_configuration. Use the visible constraints as the checklist for names, values and references before you run the tests.

**When to use it:** Use S3 when you need durable object storage for assets, logs, backups or static content, and lock down access from the start.

**How to approach it:** Open `main.tf` and work only inside `resource "aws_s3_bucket_server_side_encryption_configuration" "this"`. Use this code shape: bucket; rule { apply_server_side_encryption_by_default { sse_algorithm } }. Use the already-declared references instead of hardcoded values: `var.bucket_name`. Keep the block header and braces, indent nested blocks by two spaces, and add one argument or nested block at a time. Run the tests after each small change so the first failure points at the next name to fix.


## Constraints

- Provider: aws (region from var.aws_region).
- Create exactly one resource of type aws_s3_bucket_server_side_encryption_configuration.
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

- `aws_s3_bucket_server_side_encryption_configuration`

## Expected outputs

- (none)

## How to test

```powershell
python judge.py test 71 --dir workspaces/071-provision-s3-encryption
```

> Hidden test details are only revealed after a submission.
