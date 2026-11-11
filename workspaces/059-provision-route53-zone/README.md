# 059 - Provision Route 53 Hosted Zone

**Level:** Level 2 - First Resources  
**Difficulty:** Easy  
**Points:** 50  
**Tags:** aws, route53, provisioning

## Scenario

Your platform team needs Route 53 Hosted Zone for authoritative DNS for a domain. Write a reusable Terraform configuration that provisions it, drives every input through variables, applies the standard tags, and exports the operational identifiers.

## What to complete

- File: `main.tf`
- Task: Complete the aws_route53_zone resource
- Add the arguments and nested blocks required for aws_route53_zone.

## Constraints

- Provider: aws (region from var.aws_region).
- Create exactly one resource of type aws_route53_zone.
- All configurable values must come from variables declared in variables.tf.
- No hardcoded AWS credentials.
- Code must pass terraform fmt conventions (2-space indents, trailing newline, no tabs).
- Tag the resource with Project, Environment and ManagedBy = "terraform".
- Expose outputs: zone_id.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `domain_name` | `string` | `example.com` |
| `environment` | `string` | `dev` |
| `project_name` | `string` | `terraform-practice` |
| `aws_region` | `string` | `us-east-1` |

## Expected resources

- `aws_route53_zone`

## Expected outputs

- `zone_id`

## How to test

```powershell
python judge.py test 59 --dir workspaces/059-provision-route53-zone
```

> Hidden test details are only revealed after a submission.
