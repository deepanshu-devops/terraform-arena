# 059 - Provision Secrets Manager Secret

**Level:** Level 2 - First Resources  
**Difficulty:** Easy  
**Points:** 50  
**Tags:** aws, secrets-manager, provisioning

## Scenario

Your platform team needs Secrets Manager Secret for secure storage for application credentials. Write a reusable Terraform configuration that provisions it, drives every input through variables, applies the standard tags, and exports the operational identifiers.

## What to complete

- File: `main.tf`
- Task: Complete the aws_secretsmanager_secret resource
- Add the arguments and nested blocks required for aws_secretsmanager_secret.

## Constraints

- Provider: aws (region from var.aws_region).
- Create exactly one resource of type aws_secretsmanager_secret.
- All configurable values must come from variables declared in variables.tf.
- No hardcoded AWS credentials.
- Code must pass terraform fmt conventions (2-space indents, trailing newline, no tabs).
- Tag the resource with Project, Environment and ManagedBy = "terraform".
- Expose outputs: secret_arn.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `secret_name` | `string` | `app/credentials` |
| `environment` | `string` | `dev` |
| `project_name` | `string` | `terraform-practice` |
| `aws_region` | `string` | `us-east-1` |

## Expected resources

- `aws_secretsmanager_secret`

## Expected outputs

- `secret_arn`

## How to test

```powershell
python judge.py test 59 --dir workspaces/059-provision-secretsmanager-secret
```

> Hidden test details are only revealed after a submission.
