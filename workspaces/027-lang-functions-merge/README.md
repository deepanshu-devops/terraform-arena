# 027 - Compose Tags With merge()

**Level:** Level 1 - Terraform Language  
**Difficulty:** Easy  
**Points:** 55  
**Tags:** terraform, functions, tags

## Scenario

Use merge() to combine a shared tag map with resource-specific tags.

## What to complete

- File: `main.tf`
- Task: Complete the locals block
- Build local.common_tags with merge() and reuse it on the bucket.

## Hints

**Why it matters:** Built-in functions keep transformations declarative. They make naming, tagging and collection manipulation repeatable instead of relying on manually maintained strings.

**What to do:** Complete the marked region in `main.tf`. The work is inside `locals`. Build local.common_tags with merge() and reuse it on the bucket. Use the visible constraints as the checklist for names, values and references before you run the tests.

**When to use it:** Use functions when you need to transform a value in place: join a list, change case, merge maps, build a formatted name, or choose a fallback.

**How to approach it:** Open `main.tf` and work only inside `locals`. Use this code shape: common_tags. Use the already-declared references instead of hardcoded values: `var.project_name`, `var.environment`. Keep the block header and braces, indent nested blocks by two spaces, and add one argument or nested block at a time. Run the tests after each small change so the first failure points at the next name to fix.


## Constraints

- Use merge().
- Keep Project, Environment, ManagedBy in the shared map.
- Provision an S3 bucket.

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
python judge.py test 27 --dir workspaces/027-lang-functions-merge
```

> Hidden test details are only revealed after a submission.
