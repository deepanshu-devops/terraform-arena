# 056 - Provision EFS File System

**Level:** Level 2 - First Resources  
**Difficulty:** Easy  
**Points:** 50  
**Tags:** aws, efs, provisioning

## Scenario

Your platform team needs EFS File System for shared POSIX storage for multiple compute nodes. Write a reusable Terraform configuration that provisions it, drives every input through variables, applies the standard tags, and exports the operational identifiers.

## What to complete

- File: `main.tf`
- Task: Complete the aws_efs_file_system resource
- Add the arguments and nested blocks required for aws_efs_file_system.

## Hints

**Why it matters:** `aws_efs_file_system` is a real building block in production configurations. The exercise isolates one decision so you can recognise the same shape when it appears inside a larger module.

**What to do:** Complete the marked region in `main.tf`. The work is inside `resource "aws_efs_file_system" "this"`. Add the arguments and nested blocks required for aws_efs_file_system. Use the visible constraints as the checklist for names, values and references before you run the tests.

**When to use it:** Use this pattern when the requirement is part of a reusable configuration that another person or environment must be able to reproduce.

**How to approach it:** Open `main.tf` and work only inside `resource "aws_efs_file_system" "this"`. Use this code shape: creation_token; tags; encrypted. Use the already-declared references instead of hardcoded values: `var.file_system_name`, `var.project_name`, `var.environment`. Keep the block header and braces, indent nested blocks by two spaces, and add one argument or nested block at a time. Run the tests after each small change so the first failure points at the next name to fix.


## Constraints

- Provider: aws (region from var.aws_region).
- Create exactly one resource of type aws_efs_file_system.
- All configurable values must come from variables declared in variables.tf.
- No hardcoded AWS credentials.
- Code must pass terraform fmt conventions (2-space indents, trailing newline, no tabs).
- Tag the resource with Project, Environment and ManagedBy = "terraform".
- Expose outputs: file_system_id.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `file_system_name` | `string` | `shared-assets` |
| `environment` | `string` | `dev` |
| `project_name` | `string` | `terraform-practice` |
| `aws_region` | `string` | `us-east-1` |

## Expected resources

- `aws_efs_file_system`

## Expected outputs

- `file_system_id`

## How to test

```powershell
python judge.py test 56 --dir workspaces/056-provision-efs-file-system
```

> Hidden test details are only revealed after a submission.
