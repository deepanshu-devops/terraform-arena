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

**What to do:** Complete the marked TODO in `main.tf`. Set the bucket argument from the input variable. Use the visible constraints as your checklist before you run the tests.

**When to use it:** Use separate files for variables, outputs and resources once a module grows beyond a few blocks. Keep tightly related blocks together.

**How to approach it:** Open `main.tf` and work inside the single TODO region. Change one requirement at a time: add the named block, argument or reference, then run the tests. When a check fails, match its wording to the constraints and fix only the block it names.


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
