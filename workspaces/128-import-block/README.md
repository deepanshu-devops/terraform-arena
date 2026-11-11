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

**What to do:** Complete the marked region in `main.tf`. The work is inside `import`. Give the real bucket id and the Terraform address it should be imported to. Use the visible constraints as the checklist for names, values and references before you run the tests.

**When to use it:** Use a remote backend for any shared or production configuration. Local state is fine only for short-lived experiments.

**How to approach it:** Open `main.tf` and work only inside `import`. Use this code shape: id; to. Use the already-declared references instead of hardcoded values: `aws_s3_bucket.this`. Keep the block header and braces, indent nested blocks by two spaces, and add one argument or nested block at a time. Run the tests after each small change so the first failure points at the next name to fix.


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
