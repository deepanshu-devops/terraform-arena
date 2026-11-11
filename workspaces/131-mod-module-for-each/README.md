# 131 - Module for_each

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

## Hints

**Why it matters:** Modules package a group of resources behind a small input/output contract. They turn copy-pasted infrastructure into something a team can version, review and reuse.

**What to do:** Complete the marked TODO in `main.tf`. Instantiate the module once per environment with for_each. Use the visible constraints as your checklist before you run the tests.

**When to use it:** Use a module when the same group of resources appears more than once, when a team needs a supported interface, or when you want to test a component independently.

**How to approach it:** Open `main.tf` and work inside the single TODO region. Change one requirement at a time: add the named block, argument or reference, then run the tests. When a check fails, match its wording to the constraints and fix only the block it names.


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
python judge.py test 131 --dir workspaces/131-mod-module-for-each
```

> Hidden test details are only revealed after a submission.
