# 044 - Provision Internet Gateway

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
python judge.py test 44 --dir workspaces/044-provision-internet-gateway
```

> Hidden test details are only revealed after a submission.
