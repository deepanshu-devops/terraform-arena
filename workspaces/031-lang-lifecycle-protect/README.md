# 031 - Protect a Bucket With prevent_destroy

**Level:** Level 1 - Terraform Language  
**Difficulty:** Easy  
**Points:** 55  
**Tags:** terraform, lifecycle, safety

## Scenario

Make sure the production bucket cannot be destroyed by an accidental terraform destroy.

## What to complete

- File: `main.tf`
- Task: Complete the lifecycle block
- Protect the bucket from accidental deletion with prevent_destroy.

## Hints

**Why it matters:** `aws_s3_bucket` is a real building block in production configurations. The exercise isolates one decision so you can recognise the same shape when it appears inside a larger module.

**What to do:** Complete the marked TODO in `main.tf`. Protect the bucket from accidental deletion with prevent_destroy. Use the visible constraints as your checklist before you run the tests.

**When to use it:** Use this pattern when the requirement is part of a reusable configuration that another person or environment must be able to reproduce.

**How to approach it:** Open `main.tf` and work inside the single TODO region. Change one requirement at a time: add the named block, argument or reference, then run the tests. When a check fails, match its wording to the constraints and fix only the block it names.


## Constraints

- Add a lifecycle block.
- prevent_destroy = true.
- Provision an S3 bucket.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `bucket_name` | `string` | `required` |

## Expected resources

- `aws_s3_bucket`

## Expected outputs

- `bucket_id`

## How to test

```powershell
python judge.py test 31 --dir workspaces/031-lang-lifecycle-protect
```

> Hidden test details are only revealed after a submission.
