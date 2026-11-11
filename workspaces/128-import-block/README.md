# 128 - Import Existing Resources

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

## Hints

**Why it matters:** State is Terraform's record of what it manages. A remote, locked and encrypted backend protects that record when more than one person or automation runs Terraform.

**What to do:** Complete the marked TODO in `main.tf`. Give the real bucket id and the Terraform address it should be imported to. Use the visible constraints as your checklist before you run the tests.

**When to use it:** Use a remote backend for any shared or production configuration. Local state is fine only for short-lived experiments.

**How to approach it:** Open `main.tf` and work inside the single TODO region. Change one requirement at a time: add the named block, argument or reference, then run the tests. When a check fails, match its wording to the constraints and fix only the block it names.


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
python judge.py test 128 --dir workspaces/128-import-block
```

> Hidden test details are only revealed after a submission.
