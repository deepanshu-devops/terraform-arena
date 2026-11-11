# 127 - Call a Local Module

**Level:** Level 5 - Modules & Capstones  
**Difficulty:** Medium  
**Points:** 80  
**Tags:** terraform, modules

## Scenario

Refactor an S3 bucket into a local module and call it from the root configuration.

## What to complete

- File: `main.tf`
- Task: Complete the module call
- Point the module at ./modules/s3 and pass the bucket inputs.

## Hints

**Why it matters:** Modules package a group of resources behind a small input/output contract. They turn copy-pasted infrastructure into something a team can version, review and reuse.

**What to do:** Complete the marked TODO in `main.tf`. Point the module at ./modules/s3 and pass the bucket inputs. Use the visible constraints as your checklist before you run the tests.

**When to use it:** Use a module when the same group of resources appears more than once, when a team needs a supported interface, or when you want to test a component independently.

**How to approach it:** Open `main.tf` and work inside the single TODO region. Change one requirement at a time: add the named block, argument or reference, then run the tests. When a check fails, match its wording to the constraints and fix only the block it names.


## Constraints

- Create a module block.
- source points at ./modules/s3.
- Pass inputs through the module.

## Input variables

| Name | Type | Default |
| --- | --- | --- |

## Expected resources

- `module`

## Expected outputs

- (none)

## How to test

```powershell
python judge.py test 127 --dir workspaces/127-mod-local-module
```

> Hidden test details are only revealed after a submission.
