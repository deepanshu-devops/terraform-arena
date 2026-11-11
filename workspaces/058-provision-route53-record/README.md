# 058 - Provision Route 53 A Record

**Level:** Level 2 - First Resources  
**Difficulty:** Easy  
**Points:** 50  
**Tags:** aws, route53, provisioning

## Scenario

Your platform team needs Route 53 A Record for pointing a hostname at an address. Write a reusable Terraform configuration that provisions it, drives every input through variables, applies the standard tags, and exports the operational identifiers.

## What to complete

- File: `main.tf`
- Task: Complete the aws_route53_record resource
- Add the arguments and nested blocks required for aws_route53_record.

## Constraints

- Provider: aws (region from var.aws_region).
- Create exactly one resource of type aws_route53_record.
- All configurable values must come from variables declared in variables.tf.
- No hardcoded AWS credentials.
- Code must pass terraform fmt conventions (2-space indents, trailing newline, no tabs).
- Expose outputs: fqdn.
- Allowed supporting resources: aws_route53_zone.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `zone_id` | `string` | `required` |
| `record_name` | `string` | `app` |
| `record_value` | `string` | `203.0.113.10` |
| `aws_region` | `string` | `us-east-1` |

## Expected resources

- `aws_route53_record`

## Expected outputs

- `fqdn`

## How to test

```powershell
python judge.py test 58 --dir workspaces/058-provision-route53-record
```

> Hidden test details are only revealed after a submission.
