# 079 - Provision VPC

**Level:** Level 2 - First Resources  
**Difficulty:** Easy  
**Points:** 50  
**Tags:** aws, vpc, provisioning

## Scenario

Your platform team needs VPC for an isolated network boundary for a workload. Write a reusable Terraform configuration that provisions it, drives every input through variables, applies the standard tags, and exports the operational identifiers.

## What to complete

- File: `main.tf`
- Task: Complete the aws_vpc resource
- Add the arguments and nested blocks required for aws_vpc.

## Hints

**Why it matters:** A VPC is the network boundary for most AWS resources. CIDR planning, subnets and routing decisions affect everything deployed inside it.

**What to do:** Complete the marked region in `main.tf`. The work is inside `resource "aws_vpc" "this"`. Add the arguments and nested blocks required for aws_vpc. Use the visible constraints as the checklist for names, values and references before you run the tests.

**When to use it:** Design a VPC when you need isolated networking, predictable address space or control over public and private traffic.

**How to approach it:** Open `main.tf` and work only inside `resource "aws_vpc" "this"`. Use this code shape: cidr_block; tags; enable_dns_support; enable_dns_hostnames. Use the already-declared references instead of hardcoded values: `var.vpc_cidr`, `var.project_name`, `var.environment`. Keep the block header and braces, indent nested blocks by two spaces, and add one argument or nested block at a time. Run the tests after each small change so the first failure points at the next name to fix.


## Constraints

- Provider: aws (region from var.aws_region).
- Create exactly one resource of type aws_vpc.
- All configurable values must come from variables declared in variables.tf.
- No hardcoded AWS credentials.
- Code must pass terraform fmt conventions (2-space indents, trailing newline, no tabs).
- Tag the resource with Project, Environment and ManagedBy = "terraform".
- Expose outputs: vpc_id.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `vpc_cidr` | `string` | `10.0.0.0/16` |
| `environment` | `string` | `dev` |
| `project_name` | `string` | `terraform-practice` |
| `aws_region` | `string` | `us-east-1` |

## Expected resources

- `aws_vpc`

## Expected outputs

- `vpc_id`

## How to test

```powershell
python judge.py test 79 --dir workspaces/079-provision-vpc
```

> Hidden test details are only revealed after a submission.
