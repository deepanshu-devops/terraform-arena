# 016 - Tutorial: Reuse a Value With a Variable

**Level:** Level 0 - HCL Foundations  
**Difficulty:** Easy  
**Points:** 64  
**Tags:** terraform, tutorial, variables

## Scenario

Welcome to the guided track. A variable is a named input: the caller can change it without editing the block that uses it. Declare one input variable and expose it through an output.

## What to complete

- File: `variables.tf`
- Task: Declare the input variable
- Add the variable metadata, its type and a default value.

## Hints

**Why it matters:** Variables are the seam between a reusable configuration and the environment that calls it. Once a value is an input, changing environments does not require editing resource code.

**What to do:** Complete the variable block in variables.tf. It needs a description, a string type and the default shown in the constraints. The output already shows how the caller reads it.

**When to use it:** Reach for an input variable when a value changes per environment, must be supplied securely, or should be controlled by whoever calls the configuration.

**How to approach it:** Start at the top of the `variable "app_name"` block. Add `description`, `type = string`, and `default`; keep the quotes around the default because it is a string. Run the tests and compare each failure with the constraint list.


## Constraints

- Declare variable app_name.
- Use type string and default demo-app.
- Create output app_name that reads var.app_name.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `app_name` | `string` | `demo-app` |

## Expected resources

- (see constraints)

## Expected outputs

- `app_name`

## How to test

```powershell
python judge.py test 16 --dir workspaces/016-tut-variable-first
```

> Hidden test details are only revealed after a submission.
