# 029 - Provision CloudFront Distribution

**Level:** Level 2 - First Resources  
**Difficulty:** Easy  
**Points:** 50  
**Tags:** aws, cloudfront, provisioning

## Scenario

Your platform team needs CloudFront Distribution for a global CDN in front of an origin. Write a reusable Terraform configuration that provisions it, drives every input through variables, applies the standard tags, and exports the operational identifiers.

## What to complete

- File: `main.tf`
- Task: Complete the aws_cloudfront_distribution resource
- Add the arguments and nested blocks required for aws_cloudfront_distribution.

## Constraints

- Provider: aws (region from var.aws_region).
- Create exactly one resource of type aws_cloudfront_distribution.
- All configurable values must come from variables declared in variables.tf.
- No hardcoded AWS credentials.
- Code must pass terraform fmt conventions (2-space indents, trailing newline, no tabs).
- Tag the resource with Project, Environment and ManagedBy = "terraform".
- Expose outputs: domain_name.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `origin_domain_name` | `string` | `example.com` |
| `certificate_arn` | `string` | `required` |
| `environment` | `string` | `dev` |
| `project_name` | `string` | `terraform-practice` |
| `aws_region` | `string` | `us-east-1` |

## Expected resources

- `aws_cloudfront_distribution`

## Expected outputs

- `domain_name`

## How to test

```powershell
python judge.py test 29 --dir workspaces/029-provision-cloudfront
```

> Hidden test details are only revealed after a submission.
