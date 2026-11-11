# 079 - Provision Cognito User Pool

**Level:** Level 3 - Real Infrastructure  
**Difficulty:** Medium  
**Points:** 80  
**Tags:** aws, cognito, provisioning

## Scenario

Your platform team needs Cognito User Pool for managed authentication for an application. Write a reusable Terraform configuration that provisions it, drives every input through variables, applies the standard tags, and exports the operational identifiers.

## What to complete

- File: `main.tf`
- Task: Complete the aws_cognito_user_pool resource
- Add the arguments and nested blocks required for aws_cognito_user_pool.

## Constraints

- Provider: aws (region from var.aws_region).
- Create exactly one resource of type aws_cognito_user_pool.
- All configurable values must come from variables declared in variables.tf.
- No hardcoded AWS credentials.
- Code must pass terraform fmt conventions (2-space indents, trailing newline, no tabs).
- Tag the resource with Project, Environment and ManagedBy = "terraform".
- Expose outputs: user_pool_arn.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `user_pool_name` | `string` | `app-users` |
| `environment` | `string` | `dev` |
| `project_name` | `string` | `terraform-practice` |
| `aws_region` | `string` | `us-east-1` |

## Expected resources

- `aws_cognito_user_pool`

## Expected outputs

- `user_pool_arn`

## How to test

```powershell
python judge.py test 79 --dir workspaces/079-provision-cognito-user-pool
```

> Hidden test details are only revealed after a submission.
