# 113 - Module for_each

**Level:** Level 5 - Modules & Capstones  
**Difficulty:** Hard  
**Points:** 100  
**Tags:** terraform, modules, for_each

## Scenario

Instantiate the same module once per environment using for_each over a map.

## What to complete

- File: `main.tf`
- Task: Complete the for_each module call
- Instantiate the module once per environment with for_each.

## Constraints

- Use module with for_each.
- Reference each.key/each.value.
- Do not hardcode environment names.

## Input variables

| Name | Type | Default |
| --- | --- | --- |

## Expected resources

- `module`

## Expected outputs

- (none)

## How to test

```powershell
python judge.py test 113 --dir workspaces/113-mod-module-for-each
```

> Hidden test details are only revealed after a submission.
