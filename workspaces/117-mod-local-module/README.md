# 117 - Call a Local Module

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
python judge.py test 117 --dir workspaces/117-mod-local-module
```

> Hidden test details are only revealed after a submission.
