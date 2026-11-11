# 015 - Resource Arguments and Tags

**Level:** Level 0 - HCL Foundations  
**Difficulty:** Easy  
**Points:** 63  
**Tags:** terraform, hcl, resources, tags

## Scenario

Resources are blocks with a type and a name. Complete an S3 bucket so the bucket name comes from a variable and the resource carries a Project tag.

## What to complete

- File: `main.tf`
- Task: Complete the bucket resource
- Set the bucket argument and add the Project tag.

## Constraints

- Keep the aws_s3_bucket resource.
- Set bucket from var.bucket_name.
- Add a tags map with Project = "arena".

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `bucket_name` | `string` | `terraform-arena-logs` |

## Expected resources

- `aws_s3_bucket`

## Expected outputs

- (none)

## How to test

```powershell
python judge.py test 15 --dir workspaces/015-intro-resource-tags
```

> Hidden test details are only revealed after a submission.
