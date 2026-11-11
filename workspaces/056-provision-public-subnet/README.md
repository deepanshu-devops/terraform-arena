# 056 - Provision Public Subnet

**Level:** Level 2 - First Resources  
**Difficulty:** Easy  
**Points:** 50  
**Tags:** aws, vpc, provisioning

## Scenario

Your platform team needs Public Subnet for a public subnet that auto-assigns IPs. Write a reusable Terraform configuration that provisions it, drives every input through variables, applies the standard tags, and exports the operational identifiers.

## What to complete

- File: `main.tf`
- Task: Complete the aws_subnet resource
- Add the arguments and nested blocks required for aws_subnet.

## Constraints

- Provider: aws (region from var.aws_region).
- Create exactly one resource of type aws_subnet.
- All configurable values must come from variables declared in variables.tf.
- No hardcoded AWS credentials.
- Code must pass terraform fmt conventions (2-space indents, trailing newline, no tabs).
- Tag the resource with Project, Environment and ManagedBy = "terraform".
- Expose outputs: subnet_id.
- Allowed supporting resources: aws_vpc.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `vpc_id` | `string` | `required` |
| `subnet_cidr` | `string` | `10.0.1.0/24` |
| `availability_zone` | `string` | `us-east-1a` |
| `environment` | `string` | `dev` |
| `project_name` | `string` | `terraform-practice` |
| `aws_region` | `string` | `us-east-1` |

## Expected resources

- `aws_subnet`

## Expected outputs

- `subnet_id`

## How to test

```powershell
python judge.py test 56 --dir workspaces/056-provision-public-subnet
```

> Hidden test details are only revealed after a submission.
