# 041 - Provision EC2 Instance

**Level:** Level 2 - First Resources  
**Difficulty:** Easy  
**Points:** 50  
**Tags:** aws, ec2, provisioning

## Scenario

Your platform team needs EC2 Instance for a virtual machine for a stateless service. Write a reusable Terraform configuration that provisions it, drives every input through variables, applies the standard tags, and exports the operational identifiers.

## What to complete

- File: `main.tf`
- Task: Complete the aws_instance resource
- Add the arguments and nested blocks required for aws_instance.

## Constraints

- Provider: aws (region from var.aws_region).
- Create exactly one resource of type aws_instance.
- All configurable values must come from variables declared in variables.tf.
- No hardcoded AWS credentials.
- Code must pass terraform fmt conventions (2-space indents, trailing newline, no tabs).
- Tag the resource with Project, Environment and ManagedBy = "terraform".
- Expose outputs: instance_id.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `ami_id` | `string` | `required` |
| `instance_type` | `string` | `t2.micro` |
| `subnet_id` | `string` | `required` |
| `environment` | `string` | `dev` |
| `project_name` | `string` | `terraform-practice` |
| `aws_region` | `string` | `us-east-1` |

## Expected resources

- `aws_instance`

## Expected outputs

- `instance_id`

## How to test

```powershell
python judge.py test 41 --dir workspaces/041-provision-ec2-instance
```

> Hidden test details are only revealed after a submission.
