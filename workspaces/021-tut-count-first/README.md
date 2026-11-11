# 021 - Tutorial: Repeat a Resource With count

**Level:** Level 0 - HCL Foundations  
**Difficulty:** Easy  
**Points:** 69  
**Tags:** terraform, tutorial, count, aws, s3

## Scenario

count creates several instances of one resource block. Each instance gets an index, which you can use to pick the matching value from a list. Create one bucket per entry in a list.

## What to complete

- File: `main.tf`
- Task: Repeat the bucket
- Add the repetition count and select a name for each instance.

## Hints

**Why it matters:** count is the smallest step from one resource to many. It also reveals why Terraform addresses instances by index, which is useful when you later compare count with for_each.

**What to do:** Complete the bucket resource body. It needs one argument that creates one instance per list entry and one argument that picks the matching name for the current instance.

**When to use it:** Use count when the instances are interchangeable and the list order is stable. If each instance has a durable name, for_each is safer.

**How to approach it:** Find the resource block and add the two arguments that depend on the list. One makes the number of instances, the other reads the current position. The output already shows how to collect every instance.


## Constraints

- Keep the aws_s3_bucket resource block.
- Set count from the length of var.bucket_names.
- Select each name with count.index.
- Export the bucket ids.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `bucket_names` | `list(string)` | `['arena-demo-one', 'arena-demo-two']` |
| `aws_region` | `string` | `us-east-1` |

## Expected resources

- `aws_s3_bucket`

## Expected outputs

- `bucket_ids`

## How to test

```powershell
python judge.py test 21 --dir workspaces/021-tut-count-first
```

> Hidden test details are only revealed after a submission.
