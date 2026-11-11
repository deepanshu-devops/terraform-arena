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

**What to do:** Complete the marked region in `main.tf`. The work is inside `locals`. Define local.common_tags and merge the standard tags into it. Use the visible constraints as the checklist for names, values and references before you run the tests.

**When to use it:** Use locals for values computed from variables, constants reused in several places, or a common map such as tags. Do not use a local for something the caller must be able to change.

**How to approach it:** Open `main.tf` and work only inside `locals`. Use this code shape: common_tags. Use the already-declared references instead of hardcoded values: `var.project_name`, `var.environment`. Keep the block header and braces, indent nested blocks by two spaces, and add one argument or nested block at a time. Run the tests after each small change so the first failure points at the next name to fix.


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
