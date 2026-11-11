# 029 - Provision ACM Certificate

**Level:** Level 2 - First Resources  
**Difficulty:** Easy  
**Points:** 50  
**Tags:** aws, acm, provisioning

## Scenario

Your platform team needs ACM Certificate for a DNS-validated TLS certificate. Write a reusable Terraform configuration that provisions it, drives every input through variables, applies the standard tags, and exports the operational identifiers.

## What to complete

- File: `main.tf`
- Task: Complete the aws_acm_certificate resource
- Add the arguments and nested blocks required for aws_acm_certificate.

## Constraints

- Provider: aws (region from var.aws_region).
- Create exactly one resource of type aws_acm_certificate.
- All configurable values must come from variables declared in variables.tf.
- No hardcoded AWS credentials.
- Code must pass terraform fmt conventions (2-space indents, trailing newline, no tabs).
- Tag the resource with Project, Environment and ManagedBy = "terraform".
- Expose outputs: certificate_arn.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `domain_name` | `string` | `example.com` |
| `environment` | `string` | `dev` |
| `project_name` | `string` | `terraform-practice` |
| `aws_region` | `string` | `us-east-1` |

## Expected resources

- `aws_acm_certificate`

## Expected outputs

- `certificate_arn`

## How to test

```powershell
python judge.py test 29 --dir workspaces/029-provision-acm-certificate
```

> Hidden test details are only revealed after a submission.
