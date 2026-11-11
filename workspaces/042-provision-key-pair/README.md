# 042 - Provision EC2 Key Pair

**Level:** Level 2 - First Resources  
**Difficulty:** Easy  
**Points:** 50  
**Tags:** aws, ec2, provisioning

## Scenario

Your platform team needs EC2 Key Pair for SSH access material for instances. Write a reusable Terraform configuration that provisions it, drives every input through variables, applies the standard tags, and exports the operational identifiers.

## What to complete

- File: `main.tf`
- Task: Complete the aws_key_pair resource
- Add the arguments and nested blocks required for aws_key_pair.

## Constraints

- Provider: aws (region from var.aws_region).
- Create exactly one resource of type aws_key_pair.
- All configurable values must come from variables declared in variables.tf.
- No hardcoded AWS credentials.
- Code must pass terraform fmt conventions (2-space indents, trailing newline, no tabs).
- Tag the resource with Project, Environment and ManagedBy = "terraform".
- Expose outputs: key_name.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `key_name` | `string` | `app-key` |
| `public_key` | `string` | `required` |
| `environment` | `string` | `dev` |
| `project_name` | `string` | `terraform-practice` |
| `aws_region` | `string` | `us-east-1` |

## Expected resources

- `aws_key_pair`

## Expected outputs

- `key_name`

## How to test

```powershell
python judge.py test 42 --dir workspaces/042-provision-key-pair
```

> Hidden test details are only revealed after a submission.
