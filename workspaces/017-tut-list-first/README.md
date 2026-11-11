# 017 - Tutorial: Work With a List

**Level:** Level 0 - HCL Foundations  
**Difficulty:** Easy  
**Points:** 65  
**Tags:** terraform, tutorial, collections

## Scenario

A list keeps values in order. Terraform can index a list, count it, or iterate over it. Build a small list of environment names and read the first item and the length.

## What to complete

- File: `main.tf`
- Task: Create the ordered list
- Add three environment names in deployment order.

## Hints

**Why it matters:** Lists are the starting point for repetition in Terraform. Indexing teaches that positions matter; length teaches how a configuration can adapt when the list grows.

**What to do:** Add one local named environments. It should contain three strings in order, starting with dev and ending with prod. The two outputs are already wired to demonstrate indexing and length.

**When to use it:** Use a list when values have a natural order or when every item is interchangeable. If each item needs a stable name, a map is usually a better fit.

**How to approach it:** Write the list with square brackets and commas. Read the output blocks first to see exactly how the list is consumed, then fill in the middle so those expressions have something to reference.


## Constraints

- Define local.environments as a list of three names.
- The first value must be dev and the last must be prod.
- Output first_environment as local.environments[0].
- Output environment_count with length(local.environments).

## Input variables

| Name | Type | Default |
| --- | --- | --- |

## Expected resources

- (see constraints)

## Expected outputs

- `first_environment`
- `environment_count`

## How to test

```powershell
python judge.py test 17 --dir workspaces/017-tut-list-first
```

> Hidden test details are only revealed after a submission.
