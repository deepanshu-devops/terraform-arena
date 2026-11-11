# 023 - Tutorial: Call Your First Module

**Level:** Level 0 - HCL Foundations  
**Difficulty:** Easy  
**Points:** 71  
**Tags:** terraform, tutorial, modules

## Scenario

A module is a reusable package of Terraform files with inputs and outputs. Calling one is just a module block: a name, a source and the inputs the module expects.

## What to complete

- File: `main.tf`
- Task: Complete the module call
- Add the module source and pass the bucket name input.

## Hints

**Why it matters:** Modules are how Terraform code scales beyond a single file. A module call lets you reuse a tested component without copying its resources.

**What to do:** Complete the module block so it loads the local storage module and passes the one input that module expects.

**When to use it:** Use a module when a group of resources is reused or when a team needs a stable interface. A local source is ideal while developing the module in the same repository.

**How to approach it:** Inside `module "storage"`, set `source` to the local `./modules/storage` path as a quoted string. Pass `bucket_name = var.bucket_name`; the argument name must match the `variable` block inside the module.


## Constraints

- Create a module block named storage.
- Point source at ./modules/storage.
- Pass var.bucket_name as bucket_name.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `bucket_name` | `string` | `arena-tutorial-storage` |

## Expected resources

- (see constraints)

## Expected outputs

- (none)

## How to test

```powershell
python judge.py test 23 --dir workspaces/023-tut-module-call
```

> Hidden test details are only revealed after a submission.
