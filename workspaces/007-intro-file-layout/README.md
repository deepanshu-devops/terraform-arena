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

## Hints

**Why it matters:** Splitting a configuration by purpose makes reviews and ownership easier. Terraform loads every .tf file in a directory as one module, so the file layout is for humans, not the engine.

**What to do:** Complete the marked region in `main.tf`. The work is inside `resource "aws_s3_bucket" "this"`. Set the bucket argument from the input variable. Use the visible constraints as the checklist for names, values and references before you run the tests.

**When to use it:** Use separate files for variables, outputs and resources once a module grows beyond a few blocks. Keep tightly related blocks together.

**How to approach it:** Open `main.tf` and work only inside `resource "aws_s3_bucket" "this"`. Use this code shape: bucket. Use the already-declared references instead of hardcoded values: `var.app_name`. Keep the block header and braces, indent nested blocks by two spaces, and add one argument or nested block at a time. Run the tests after each small change so the first failure points at the next name to fix.


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
