# 118 - Import Existing Resources

**Level:** Level 5 - Modules & Capstones  
**Difficulty:** Medium  
**Points:** 80  
**Tags:** terraform, import, state

## Scenario

Bring an existing resource under Terraform management using an import block.

## What to complete

- File: `main.tf`
- Task: Complete the import block
- Give the real bucket id and the Terraform address it should be imported to.

## Constraints

- Use an import block.
- Provide id.
- Match the configuration to the imported resource.

## Input variables

| Name | Type | Default |
| --- | --- | --- |

## Expected resources

- (see constraints)

## Expected outputs

- (none)

## How to test

```powershell
python judge.py test 118 --dir workspaces/118-import-block
```

> Hidden test details are only revealed after a submission.
