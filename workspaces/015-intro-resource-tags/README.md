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

## Hints

**Why it matters:** HCL is the language Terraform evaluates. Small syntax mistakes here turn into confusing plan errors later, so slow, deliberate practice pays off.

**What to do:** Complete the marked TODO in `main.tf`. Set the bucket argument and add the Project tag. Use the visible constraints as your checklist before you run the tests.

**When to use it:** Reach for this whenever you add a new block or argument by hand rather than copying generated code.

**How to approach it:** Open `main.tf` and work inside the single TODO region. Change one requirement at a time: add the named block, argument or reference, then run the tests. When a check fails, match its wording to the constraints and fix only the block it names.


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
