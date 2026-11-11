# 062 - Provision Internet Gateway

**Level:** Level 2 - First Resources  
**Difficulty:** Easy  
**Points:** 50  
**Tags:** aws, vpc, provisioning

## Scenario

Your platform team needs Internet Gateway for outbound internet connectivity for a VPC. Write a reusable Terraform configuration that provisions it, drives every input through variables, applies the standard tags, and exports the operational identifiers.

## What to complete

- File: `main.tf`
- Task: Complete the aws_internet_gateway resource
- Add the arguments and nested blocks required for aws_internet_gateway.

## Hints

**Why it matters:** A VPC is the network boundary for most AWS resources. CIDR planning, subnets and routing decisions affect everything deployed inside it.

**What to do:** Complete the marked region in `main.tf`. The work is inside `resource "aws_internet_gateway" "this"`. Add the arguments and nested blocks required for aws_internet_gateway. Use the visible constraints as the checklist for names, values and references before you run the tests.

**When to use it:** Design a VPC when you need isolated networking, predictable address space or control over public and private traffic.

**How to approach it:** Open `main.tf` and work only inside `resource "aws_internet_gateway" "this"`. Use this code shape: tags; vpc_id. Use the already-declared references instead of hardcoded values: `var.project_name`, `var.environment`, `var.vpc_id`. Keep the block header and braces, indent nested blocks by two spaces, and add one argument or nested block at a time. Run the tests after each small change so the first failure points at the next name to fix.


## Constraints

- Provider: aws (region from var.aws_region).
- Create exactly one resource of type aws_internet_gateway.
- All configurable values must come from variables declared in variables.tf.
- No hardcoded AWS credentials.
- Code must pass terraform fmt conventions (2-space indents, trailing newline, no tabs).
- Tag the resource with Project, Environment and ManagedBy = "terraform".
- Expose outputs: internet_gateway_id.
- Allowed supporting resources: aws_vpc.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `vpc_id` | `string` | `required` |
| `environment` | `string` | `dev` |
| `project_name` | `string` | `terraform-practice` |
| `aws_region` | `string` | `us-east-1` |

## Expected resources

- `aws_internet_gateway`

## Expected outputs

- `internet_gateway_id`

## How to test

```powershell
python judge.py test 62 --dir workspaces/062-provision-internet-gateway
```

> Hidden test details are only revealed after a submission.
