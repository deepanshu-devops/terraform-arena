# 068 - Provision Security Group

**Level:** Level 2 - First Resources  
**Difficulty:** Easy  
**Points:** 50  
**Tags:** aws, ec2, provisioning

## Scenario

Your platform team needs Security Group for stateful firewall rules for an application. Write a reusable Terraform configuration that provisions it, drives every input through variables, applies the standard tags, and exports the operational identifiers.

## What to complete

- File: `main.tf`
- Task: Complete the aws_security_group resource
- Add the arguments and nested blocks required for aws_security_group.

## Constraints

- Provider: aws (region from var.aws_region).
- Create exactly one resource of type aws_security_group.
- All configurable values must come from variables declared in variables.tf.
- No hardcoded AWS credentials.
- Code must pass terraform fmt conventions (2-space indents, trailing newline, no tabs).
- Tag the resource with Project, Environment and ManagedBy = "terraform".
- Expose outputs: security_group_id.
- Allowed supporting resources: aws_vpc.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `vpc_id` | `string` | `required` |
| `security_group_name` | `string` | `app-sg` |
| `environment` | `string` | `dev` |
| `project_name` | `string` | `terraform-practice` |
| `aws_region` | `string` | `us-east-1` |

## Expected resources

- `aws_security_group`

## Expected outputs

- `security_group_id`

## How to test

```powershell
python judge.py test 68 --dir workspaces/068-provision-security-group
```

> Hidden test details are only revealed after a submission.
