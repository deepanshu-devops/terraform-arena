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

**What to do:** Complete the marked region in `main.tf`. The work is inside `resource "aws_s3_bucket" "this"` -> `lifecycle`. Protect the bucket from accidental deletion with prevent_destroy. Use the visible constraints as the checklist for names, values and references before you run the tests.

**When to use it:** Use this pattern when the requirement is part of a reusable configuration that another person or environment must be able to reproduce.

**How to approach it:** Open `main.tf` and work only inside `resource "aws_s3_bucket" "this"` -> `lifecycle`. Use this code shape: prevent_destroy. Keep the block header and braces, indent nested blocks by two spaces, and add one argument or nested block at a time. Run the tests after each small change so the first failure points at the next name to fix.


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
