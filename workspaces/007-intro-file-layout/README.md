# 007 - Split a Configuration Across Files

**Level:** Level 0 - HCL Foundations  
**Difficulty:** Easy  
**Points:** 55  
**Tags:** terraform, files, layout

## Scenario

Terraform reads every .tf file in a directory as one configuration. The versions, variables and outputs files are complete; finish the resource in main.tf.

## What to complete

- File: `main.tf`
- Task: Complete the bucket resource
- Set the bucket argument from the input variable.

## Constraints

- Keep the provider and versions in versions.tf.
- Use var.app_name for the bucket name.
- bucket_id must reference the bucket.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `app_name` | `string` | `terraform-arena` |
| `aws_region` | `string` | `us-east-1` |

## Expected resources

- `aws_s3_bucket`

## Expected outputs

- `bucket_id`

## How to test

```powershell
python judge.py test 7 --dir workspaces/007-intro-file-layout
```

> Hidden test details are only revealed after a submission.
