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

**What to do:** Complete the marked region in `main.tf`. The work is inside `module "this"`. Point the module at ./modules/s3 and pass the bucket inputs. Use the visible constraints as the checklist for names, values and references before you run the tests.

**When to use it:** Use a module when the same group of resources appears more than once, when a team needs a supported interface, or when you want to test a component independently.

**How to approach it:** Open `main.tf` and work only inside `module "this"`. Use this code shape: source; bucket_name; environment. Keep the block header and braces, indent nested blocks by two spaces, and add one argument or nested block at a time. Run the tests after each small change so the first failure points at the next name to fix.


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
