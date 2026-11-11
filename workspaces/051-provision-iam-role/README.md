# 051 - Provision IAM Role

**Level:** Level 2 - First Resources  
**Difficulty:** Easy  
**Points:** 50  
**Tags:** aws, iam, provisioning

## Scenario

Your platform team needs IAM Role for a service role with a trust policy. Write a reusable Terraform configuration that provisions it, drives every input through variables, applies the standard tags, and exports the operational identifiers.

## What to complete

- File: `main.tf`
- Task: Complete the aws_iam_role resource
- Add the arguments and nested blocks required for aws_iam_role.

## Constraints

- Provider: aws (region from var.aws_region).
- Create exactly one resource of type aws_iam_role.
- All configurable values must come from variables declared in variables.tf.
- No hardcoded AWS credentials.
- Code must pass terraform fmt conventions (2-space indents, trailing newline, no tabs).
- Tag the resource with Project, Environment and ManagedBy = "terraform".
- Expose outputs: role_arn.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `role_name` | `string` | `app-role` |
| `trusted_service` | `string` | `lambda.amazonaws.com` |
| `environment` | `string` | `dev` |
| `project_name` | `string` | `terraform-practice` |
| `aws_region` | `string` | `us-east-1` |

## Expected resources

- `aws_iam_role`

## Expected outputs

- `role_arn`

## How to test

```powershell
python judge.py test 51 --dir workspaces/051-provision-iam-role
```

> Hidden test details are only revealed after a submission.
