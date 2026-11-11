# 076 - Provision Lambda Function

**Level:** Level 3 - Real Infrastructure  
**Difficulty:** Medium  
**Points:** 70  
**Tags:** aws, lambda, provisioning

## Scenario

Your platform team needs Lambda Function for an event-driven Python function. Write a reusable Terraform configuration that provisions it, drives every input through variables, applies the standard tags, and exports the operational identifiers.

## What to complete

- File: `main.tf`
- Task: Complete the aws_lambda_function resource
- Add the arguments and nested blocks required for aws_lambda_function.

## Constraints

- Provider: aws (region from var.aws_region).
- Create exactly one resource of type aws_lambda_function.
- All configurable values must come from variables declared in variables.tf.
- No hardcoded AWS credentials.
- Code must pass terraform fmt conventions (2-space indents, trailing newline, no tabs).
- Tag the resource with Project, Environment and ManagedBy = "terraform".
- Expose outputs: lambda_arn.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `lambda_role_arn` | `string` | `required` |
| `lambda_runtime` | `string` | `python3.12` |
| `lambda_memory` | `number` | `128` |
| `environment` | `string` | `dev` |
| `project_name` | `string` | `terraform-practice` |
| `aws_region` | `string` | `us-east-1` |

## Expected resources

- `aws_lambda_function`

## Expected outputs

- `lambda_arn`

## How to test

```powershell
python judge.py test 76 --dir workspaces/076-provision-lambda-function
```

> Hidden test details are only revealed after a submission.
