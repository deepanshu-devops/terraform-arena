# 069 - Provision VPC

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
python judge.py test 69 --dir workspaces/069-provision-vpc
```

> Hidden test details are only revealed after a submission.
