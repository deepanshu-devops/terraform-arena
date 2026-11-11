# 031 - Provision ALB Target Group

**Level:** Level 2 - First Resources  
**Difficulty:** Easy  
**Points:** 50  
**Tags:** aws, alb, provisioning

## Scenario

Your platform team needs ALB Target Group for health-checked backend targets. Write a reusable Terraform configuration that provisions it, drives every input through variables, applies the standard tags, and exports the operational identifiers.

## What to complete

- File: `main.tf`
- Task: Complete the aws_lb_target_group resource
- Add the arguments and nested blocks required for aws_lb_target_group.

## Constraints

- Provider: aws (region from var.aws_region).
- Create exactly one resource of type aws_lb_target_group.
- All configurable values must come from variables declared in variables.tf.
- No hardcoded AWS credentials.
- Code must pass terraform fmt conventions (2-space indents, trailing newline, no tabs).
- Tag the resource with Project, Environment and ManagedBy = "terraform".
- Expose outputs: target_group_arn.
- Allowed supporting resources: aws_vpc.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `vpc_id` | `string` | `required` |
| `environment` | `string` | `dev` |
| `project_name` | `string` | `terraform-practice` |
| `aws_region` | `string` | `us-east-1` |

## Expected resources

- `aws_lb_target_group`

## Expected outputs

- `target_group_arn`

## How to test

```powershell
python judge.py test 31 --dir workspaces/031-provision-target-group
```

> Hidden test details are only revealed after a submission.
