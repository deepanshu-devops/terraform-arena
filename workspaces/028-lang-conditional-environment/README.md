# 028 - Conditional Expressions

**Level:** Level 1 - Terraform Language  
**Difficulty:** Easy  
**Points:** 55  
**Tags:** terraform, conditionals

## Scenario

Use a conditional expression to choose a bucket name suffix or retention value based on var.environment.

## What to complete

- File: `main.tf`
- Task: Complete the bucket name expression
- Use a conditional expression so production keeps the base name and other environments get a suffix.

## Hints

**Why it matters:** A conditional expression lets one configuration express a small policy difference without duplicating a whole file. That is often the cleanest way to handle environment-specific settings.

**What to do:** Complete the marked TODO in `main.tf`. Use a conditional expression so production keeps the base name and other environments get a suffix. Use the visible constraints as your checklist before you run the tests.

**When to use it:** Use a conditional when a value has two clear branches. If the branches affect whole resources or many arguments, separate configuration or a module is usually easier to maintain.

**How to approach it:** Open `main.tf` and work inside the single TODO region. Change one requirement at a time: add the named block, argument or reference, then run the tests. When a check fails, match its wording to the constraints and fix only the block it names.


## Constraints

- Use the ternary operator.
- Reference var.environment.
- Provision an S3 bucket.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `environment` | `string` | `dev` |
| `bucket_name` | `string` | `app-assets` |

## Expected resources

- `aws_s3_bucket`

## Expected outputs

- `bucket_id`

## How to test

```powershell
python judge.py test 28 --dir workspaces/028-lang-conditional-environment
```

> Hidden test details are only revealed after a submission.
