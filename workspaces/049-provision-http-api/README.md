# 049 - Provision HTTP API Gateway

**Level:** Level 2 - First Resources  
**Difficulty:** Easy  
**Points:** 50  
**Tags:** aws, api-gateway, provisioning

## Scenario

Your platform team needs HTTP API Gateway for a lightweight HTTP front door. Write a reusable Terraform configuration that provisions it, drives every input through variables, applies the standard tags, and exports the operational identifiers.

## What to complete

- File: `main.tf`
- Task: Complete the aws_apigatewayv2_api resource
- Add the arguments and nested blocks required for aws_apigatewayv2_api.

## Constraints

- Provider: aws (region from var.aws_region).
- Create exactly one resource of type aws_apigatewayv2_api.
- All configurable values must come from variables declared in variables.tf.
- No hardcoded AWS credentials.
- Code must pass terraform fmt conventions (2-space indents, trailing newline, no tabs).
- Tag the resource with Project, Environment and ManagedBy = "terraform".
- Expose outputs: api_endpoint.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `api_name` | `string` | `items-api` |
| `environment` | `string` | `dev` |
| `project_name` | `string` | `terraform-practice` |
| `aws_region` | `string` | `us-east-1` |

## Expected resources

- `aws_apigatewayv2_api`

## Expected outputs

- `api_endpoint`

## How to test

```powershell
python judge.py test 49 --dir workspaces/049-provision-http-api
```

> Hidden test details are only revealed after a submission.
