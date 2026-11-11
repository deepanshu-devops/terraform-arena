# 035 - Provision Application Load Balancer

**Level:** Level 2 - First Resources  
**Difficulty:** Easy  
**Points:** 50  
**Tags:** aws, alb, provisioning

## Scenario

Your platform team needs Application Load Balancer for distributing HTTP traffic across targets. Write a reusable Terraform configuration that provisions it, drives every input through variables, applies the standard tags, and exports the operational identifiers.

## What to complete

- File: `main.tf`
- Task: Complete the aws_lb resource
- Add the arguments and nested blocks required for aws_lb.

## Constraints

- Provider: aws (region from var.aws_region).
- Create exactly one resource of type aws_lb.
- All configurable values must come from variables declared in variables.tf.
- No hardcoded AWS credentials.
- Code must pass terraform fmt conventions (2-space indents, trailing newline, no tabs).
- Tag the resource with Project, Environment and ManagedBy = "terraform".
- Expose outputs: lb_arn, lb_dns_name.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `subnet_ids` | `list(string)` | `required` |
| `security_group_ids` | `list(string)` | `required` |
| `environment` | `string` | `dev` |
| `project_name` | `string` | `terraform-practice` |
| `aws_region` | `string` | `us-east-1` |

## Expected resources

- `aws_lb`

## Expected outputs

- `lb_arn`
- `lb_dns_name`

## How to test

```powershell
python judge.py test 35 --dir workspaces/035-provision-application-load-balancer
```

> Hidden test details are only revealed after a submission.
