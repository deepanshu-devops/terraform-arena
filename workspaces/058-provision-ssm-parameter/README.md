# 058 - Provision SSM Secure Parameter

**Level:** Level 2 - First Resources  
**Difficulty:** Easy  
**Points:** 50  
**Tags:** aws, ssm, provisioning

## Scenario

Your platform team needs SSM Secure Parameter for encrypted configuration values. Write a reusable Terraform configuration that provisions it, drives every input through variables, applies the standard tags, and exports the operational identifiers.

## What to complete

- File: `main.tf`
- Task: Complete the aws_ssm_parameter resource
- Add the arguments and nested blocks required for aws_ssm_parameter.

## Constraints

- Provider: aws (region from var.aws_region).
- Create exactly one resource of type aws_ssm_parameter.
- All configurable values must come from variables declared in variables.tf.
- No hardcoded AWS credentials.
- Code must pass terraform fmt conventions (2-space indents, trailing newline, no tabs).
- Tag the resource with Project, Environment and ManagedBy = "terraform".
- Expose outputs: parameter_arn.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `parameter_name` | `string` | `/app/config` |
| `parameter_value` | `string` | `required` |
| `environment` | `string` | `dev` |
| `project_name` | `string` | `terraform-practice` |
| `aws_region` | `string` | `us-east-1` |

## Expected resources

- `aws_ssm_parameter`

## Expected outputs

- `parameter_arn`

## How to test

```powershell
python judge.py test 58 --dir workspaces/058-provision-ssm-parameter
```

> Hidden test details are only revealed after a submission.
