# 022 - Tutorial: Name Instances With for_each

**Level:** Level 0 - HCL Foundations  
**Difficulty:** Easy  
**Points:** 70  
**Tags:** terraform, tutorial, for_each, aws, s3

## Scenario

for_each creates one instance per key in a map or set. Unlike count, each instance keeps a stable address even when the collection changes. Create one bucket for every map entry.

## What to complete

- File: `main.tf`
- Task: Create named instances
- Iterate over the map and use the current entry value as the bucket name.

## Hints

**Why it matters:** for_each protects stable addresses. Adding or removing a key changes only that key's instance, while a count list can shift every later index.

**What to do:** Complete the bucket body with a per-key iteration and a reference to the current map value. The output already shows how to reshape the resulting instances into a map.

**When to use it:** Use for_each when each instance has a meaningful key, especially when instances may be added or removed over time.

**How to approach it:** Add `for_each` over the `var.bucket_names` map, then read the current item with `each.value` in the `bucket` argument. Do not use `count.index` here; the input is keyed, and the output already iterates with `name` and `bucket`.


## Constraints

- Keep the aws_s3_bucket resource block.
- Use for_each over var.bucket_names.
- Read the bucket name from each.value.
- Export a map of bucket ids.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `bucket_names` | `map(string)` | `{'logs': 'arena-tutorial-logs', 'assets': 'arena-tutorial-assets'}` |
| `aws_region` | `string` | `us-east-1` |

## Expected resources

- `aws_s3_bucket`

## Expected outputs

- `bucket_ids`

## How to test

```powershell
python judge.py test 22 --dir workspaces/022-tut-for-each-first
```

> Hidden test details are only revealed after a submission.
