# 053 - Provision KMS Customer Key

**Level:** Level 2 - First Resources  
**Difficulty:** Easy  
**Points:** 50  
**Tags:** aws, kms, provisioning

## Scenario

Your platform team needs KMS Customer Key for a rotating customer-managed encryption key. Write a reusable Terraform configuration that provisions it, drives every input through variables, applies the standard tags, and exports the operational identifiers.

## What to complete

- File: `main.tf`
- Task: Complete the aws_kms_key resource
- Add the arguments and nested blocks required for aws_kms_key.

## Constraints

- Provider: aws (region from var.aws_region).
- Create exactly one resource of type aws_kms_key.
- All configurable values must come from variables declared in variables.tf.
- No hardcoded AWS credentials.
- Code must pass terraform fmt conventions (2-space indents, trailing newline, no tabs).
- Tag the resource with Project, Environment and ManagedBy = "terraform".
- Expose outputs: key_arn, key_id.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `environment` | `string` | `dev` |
| `project_name` | `string` | `terraform-practice` |
| `aws_region` | `string` | `us-east-1` |

## Expected resources

- `aws_kms_key`

## Expected outputs

- `key_arn`
- `key_id`

## How to test

```powershell
python judge.py test 53 --dir workspaces/053-provision-kms-key
```

> Hidden test details are only revealed after a submission.
