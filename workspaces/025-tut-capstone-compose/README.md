# 025 - Tutorial: Put It All Together

**Level:** Level 0 - HCL Foundations  
**Difficulty:** Easy  
**Points:** 73  
**Tags:** terraform, tutorial, modules, for_each, collections

## Scenario

This final tutorial step combines the ideas so far. Turn a list of environments into a map, then let a module consume that map with for_each so each environment gets its own stable instance.

## What to complete

- File: `main.tf`
- Task: Build the module input map
- Turn the environment list into a map of stable bucket names.

## Hints

**Why it matters:** This is the shape of a reusable environment pattern: a caller supplies a small list, a local derives stable keys, and a module creates one instance per key.

**What to do:** Complete the environment_map local. Every environment should become a key whose value is a project-prefixed bucket name. The module call and output below are already wired.

**When to use it:** Use this composition when several environments need the same component and you want adding an environment to be a one-line change.

**How to approach it:** Inside `locals`, add `environment_map` as a braced `for` expression over `var.environments`. Use the loop variable as both the map key and the environment name in the value, and build each value from `var.project_name` plus that name. The module call already consumes `local.environment_map`.


## Constraints

- Build local.environment_map from var.environments.
- Include var.project_name in each generated name.
- The module uses local.environment_map with for_each.
- Export the module's bucket names.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `project_name` | `string` | `arena` |
| `environments` | `list(string)` | `['dev', 'prod']` |

## Expected resources

- (see constraints)

## Expected outputs

- `bucket_names`

## How to test

```powershell
python judge.py test 25 --dir workspaces/025-tut-capstone-compose
```

> Hidden test details are only revealed after a submission.
