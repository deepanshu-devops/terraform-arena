# 046 - Provision Lambda Invoke Permission

**Level:** Level 2 - First Resources  
**Difficulty:** Easy  
**Points:** 50  
**Tags:** aws, lambda, provisioning

## Scenario

Your platform team needs Lambda Invoke Permission for allowing API Gateway to invoke a function. Write a reusable Terraform configuration that provisions it, drives every input through variables, applies the standard tags, and exports the operational identifiers.

## What to complete

- File: `main.tf`
- Task: Complete the aws_lambda_permission resource
- Add the arguments and nested blocks required for aws_lambda_permission.

## Constraints

- Provider: aws (region from var.aws_region).
- Create exactly one resource of type aws_lambda_permission.
- All configurable values must come from variables declared in variables.tf.
- No hardcoded AWS credentials.
- Code must pass terraform fmt conventions (2-space indents, trailing newline, no tabs).
- Expose outputs: statement_id.
- Allowed supporting resources: aws_lambda_function.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `lambda_function_name` | `string` | `required` |
| `aws_region` | `string` | `us-east-1` |

## Expected resources

- `aws_lambda_permission`

## Expected outputs

- `statement_id`

## How to test

```powershell
python judge.py test 46 --dir workspaces/046-provision-lambda-permission
```

> Hidden test details are only revealed after a submission.
