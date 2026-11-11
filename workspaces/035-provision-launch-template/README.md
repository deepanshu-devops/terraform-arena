# 035 - Provision EC2 Launch Template

**Level:** Level 2 - First Resources  
**Difficulty:** Easy  
**Points:** 50  
**Tags:** aws, ec2, provisioning

## Scenario

Your platform team needs EC2 Launch Template for a reusable, hardened instance blueprint. Write a reusable Terraform configuration that provisions it, drives every input through variables, applies the standard tags, and exports the operational identifiers.

## What to complete

- File: `main.tf`
- Task: Complete the aws_launch_template resource
- Add the arguments and nested blocks required for aws_launch_template.

## Constraints

- Provider: aws (region from var.aws_region).
- Create exactly one resource of type aws_launch_template.
- All configurable values must come from variables declared in variables.tf.
- No hardcoded AWS credentials.
- Code must pass terraform fmt conventions (2-space indents, trailing newline, no tabs).
- Tag the resource with Project, Environment and ManagedBy = "terraform".
- Expose outputs: launch_template_id.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `ami_id` | `string` | `required` |
| `instance_type` | `string` | `t2.micro` |
| `environment` | `string` | `dev` |
| `project_name` | `string` | `terraform-practice` |
| `aws_region` | `string` | `us-east-1` |

## Expected resources

- `aws_launch_template`

## Expected outputs

- `launch_template_id`

## How to test

```powershell
python judge.py test 35 --dir workspaces/035-provision-launch-template
```

> Hidden test details are only revealed after a submission.
