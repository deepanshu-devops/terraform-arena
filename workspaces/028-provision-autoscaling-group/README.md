# 028 - Provision Auto Scaling Group

**Level:** Level 2 - First Resources  
**Difficulty:** Easy  
**Points:** 50  
**Tags:** aws, ec2, provisioning

## Scenario

Your platform team needs Auto Scaling Group for elastic capacity across subnets. Write a reusable Terraform configuration that provisions it, drives every input through variables, applies the standard tags, and exports the operational identifiers.

## What to complete

- File: `main.tf`
- Task: Complete the aws_autoscaling_group resource
- Add the arguments and nested blocks required for aws_autoscaling_group.

## Constraints

- Provider: aws (region from var.aws_region).
- Create exactly one resource of type aws_autoscaling_group.
- All configurable values must come from variables declared in variables.tf.
- No hardcoded AWS credentials.
- Code must pass terraform fmt conventions (2-space indents, trailing newline, no tabs).
- Expose outputs: asg_name.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `asg_min` | `number` | `1` |
| `asg_max` | `number` | `2` |
| `asg_desired` | `number` | `1` |
| `subnet_ids` | `list(string)` | `required` |
| `aws_region` | `string` | `us-east-1` |

## Expected resources

- `aws_autoscaling_group`

## Expected outputs

- `asg_name`

## How to test

```powershell
python judge.py test 28 --dir workspaces/028-provision-autoscaling-group
```

> Hidden test details are only revealed after a submission.
