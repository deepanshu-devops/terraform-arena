# 030 - Locals for Common Tags

**Level:** Level 1 - Terraform Language  
**Difficulty:** Easy  
**Points:** 55  
**Tags:** terraform, locals, tags

## Scenario

Use a locals block to define common_tags and reuse it across the bucket instead of repeating tag maps.

## What to complete

- File: `main.tf`
- Task: Complete the shared tags locals block
- Define local.common_tags and merge the standard tags into it.

## Hints

**Why it matters:** Locals give a name to derived values and shared fragments. They remove repetition without making a value a user-facing input.

**What to do:** Complete the marked TODO in `main.tf`. Define local.common_tags and merge the standard tags into it. Use the visible constraints as your checklist before you run the tests.

**When to use it:** Use locals for values computed from variables, constants reused in several places, or a common map such as tags. Do not use a local for something the caller must be able to change.

**How to approach it:** Open `main.tf` and work inside the single TODO region. Change one requirement at a time: add the named block, argument or reference, then run the tests. When a check fails, match its wording to the constraints and fix only the block it names.


## Constraints

- Define local.common_tags.
- Reference local.common_tags from the bucket.
- No duplicated tag literals.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `project_name` | `string` | `terraform-practice` |
| `environment` | `string` | `dev` |

## Expected resources

- `aws_s3_bucket`

## Expected outputs

- `bucket_id`

## How to test

```powershell
python judge.py test 30 --dir workspaces/030-lang-locals-common-tags
```

> Hidden test details are only revealed after a submission.
