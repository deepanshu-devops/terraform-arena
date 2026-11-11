# 055 - Provision NAT Gateway

**Level:** Level 2 - First Resources  
**Difficulty:** Easy  
**Points:** 50  
**Tags:** aws, vpc, provisioning

## Scenario

Your platform team needs NAT Gateway for outbound internet for private subnets. Write a reusable Terraform configuration that provisions it, drives every input through variables, applies the standard tags, and exports the operational identifiers.

## What to complete

- File: `main.tf`
- Task: Complete the aws_nat_gateway resource
- Add the arguments and nested blocks required for aws_nat_gateway.

## Constraints

- Provider: aws (region from var.aws_region).
- Create exactly one resource of type aws_nat_gateway.
- All configurable values must come from variables declared in variables.tf.
- No hardcoded AWS credentials.
- Code must pass terraform fmt conventions (2-space indents, trailing newline, no tabs).
- Tag the resource with Project, Environment and ManagedBy = "terraform".
- Expose outputs: nat_gateway_id.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `eip_allocation_id` | `string` | `required` |
| `public_subnet_id` | `string` | `required` |
| `environment` | `string` | `dev` |
| `project_name` | `string` | `terraform-practice` |
| `aws_region` | `string` | `us-east-1` |

## Expected resources

- `aws_nat_gateway`

## Expected outputs

- `nat_gateway_id`

## How to test

```powershell
python judge.py test 55 --dir workspaces/055-provision-nat-gateway
```

> Hidden test details are only revealed after a submission.
