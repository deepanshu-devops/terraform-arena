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

**What to do:** Complete the marked TODO in `main.tf`. Build local.common_tags with merge() and reuse it on the bucket. Use the visible constraints as your checklist before you run the tests.

**When to use it:** Use functions when you need to transform a value in place: join a list, change case, merge maps, build a formatted name, or choose a fallback.

**How to approach it:** Open `main.tf` and work inside the single TODO region. Change one requirement at a time: add the named block, argument or reference, then run the tests. When a check fails, match its wording to the constraints and fix only the block it names.


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
