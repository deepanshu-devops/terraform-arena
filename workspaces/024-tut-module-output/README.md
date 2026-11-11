# 024 - Tutorial: Read a Module Output

**Level:** Level 0 - HCL Foundations  
**Difficulty:** Easy  
**Points:** 72  
**Tags:** terraform, tutorial, modules, outputs

## Scenario

A module can expose values to its caller through outputs. The caller reads them with module.<name>.<output>. Wire a module output to a root output so operators can see it.

## What to complete

- File: `main.tf`
- Task: Wire the module output
- Set the root output value to the module's storage_id output.

## Hints

**Why it matters:** Outputs are the contract between a module and its caller. They prevent a caller from depending on internal resource addresses, which the module should be free to change.

**What to do:** Complete the root output value. The module is already called; the only missing piece is the dotted reference that reaches its exported storage_id.

**When to use it:** Use a module output when a caller needs an identifier or setting without knowing how the module implements it.

**How to approach it:** Inside the existing root `output` block, set `value` to the module output reference. Use the module label from the `module` block and the exported name `storage_id` from the module's `outputs.tf`, joined with dots.


## Constraints

- Keep the module storage call unchanged.
- Output bucket_id from output bucket_id.
- Reference module.storage.storage_id.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `bucket_name` | `string` | `arena-tutorial-storage` |

## Expected resources

- (see constraints)

## Expected outputs

- `bucket_id`

## How to test

```powershell
python judge.py test 24 --dir workspaces/024-tut-module-output
```

> Hidden test details are only revealed after a submission.
