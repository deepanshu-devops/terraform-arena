# 052 - Provision EC2 Key Pair

**Level:** Level 2 - First Resources  
**Difficulty:** Easy  
**Points:** 50  
**Tags:** aws, ec2, provisioning

## Scenario

Your platform team needs EC2 Key Pair for SSH access material for instances. Write a reusable Terraform configuration that provisions it, drives every input through variables, applies the standard tags, and exports the operational identifiers.

## What to complete

- File: `main.tf`
- Task: Complete the aws_key_pair resource
- Add the arguments and nested blocks required for aws_key_pair.

## Hints

**Why it matters:** EC2 teaches the core lifecycle of compute: image, instance type, networking, storage and safe replacement.

**What to do:** Complete the marked region in `main.tf`. The work is inside `resource "aws_key_pair" "this"`. Add the arguments and nested blocks required for aws_key_pair. Use the visible constraints as the checklist for names, values and references before you run the tests.

**When to use it:** Use EC2 when you need a virtual machine you control directly, or as a building block inside an autoscaling or container platform.

**How to approach it:** Open `main.tf` and work only inside `resource "aws_key_pair" "this"`. Use this code shape: key_name; public_key; tags. Use the already-declared references instead of hardcoded values: `var.key_name`, `var.public_key`, `var.project_name`, `var.environment`. Keep the block header and braces, indent nested blocks by two spaces, and add one argument or nested block at a time. Run the tests after each small change so the first failure points at the next name to fix.


## Constraints

- Provider: aws (region from var.aws_region).
- Create exactly one resource of type aws_key_pair.
- All configurable values must come from variables declared in variables.tf.
- No hardcoded AWS credentials.
- Code must pass terraform fmt conventions (2-space indents, trailing newline, no tabs).
- Tag the resource with Project, Environment and ManagedBy = "terraform".
- Expose outputs: key_name.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `key_name` | `string` | `app-key` |
| `public_key` | `string` | `required` |
| `environment` | `string` | `dev` |
| `project_name` | `string` | `terraform-practice` |
| `aws_region` | `string` | `us-east-1` |

## Expected resources

- `aws_key_pair`

## Expected outputs

- `key_name`

## How to test

```powershell
python judge.py test 52 --dir workspaces/052-provision-key-pair
```

> Hidden test details are only revealed after a submission.
