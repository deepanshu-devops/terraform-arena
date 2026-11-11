# 083 - Provision WAF Web ACL

**Level:** Level 3 - Real Infrastructure  
**Difficulty:** Medium  
**Points:** 80  
**Tags:** aws, waf, provisioning

## Scenario

Your platform team needs WAF Web ACL for edge protection for public endpoints. Write a reusable Terraform configuration that provisions it, drives every input through variables, applies the standard tags, and exports the operational identifiers.

## What to complete

- File: `main.tf`
- Task: Complete the aws_wafv2_web_acl resource
- Add the arguments and nested blocks required for aws_wafv2_web_acl.

## Constraints

- Provider: aws (region from var.aws_region).
- Create exactly one resource of type aws_wafv2_web_acl.
- All configurable values must come from variables declared in variables.tf.
- No hardcoded AWS credentials.
- Code must pass terraform fmt conventions (2-space indents, trailing newline, no tabs).
- Tag the resource with Project, Environment and ManagedBy = "terraform".
- Expose outputs: web_acl_arn.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `web_acl_name` | `string` | `app-waf` |
| `environment` | `string` | `dev` |
| `project_name` | `string` | `terraform-practice` |
| `aws_region` | `string` | `us-east-1` |

## Expected resources

- `aws_wafv2_web_acl`

## Expected outputs

- `web_acl_arn`

## How to test

```powershell
python judge.py test 83 --dir workspaces/083-provision-waf-web-acl
```

> Hidden test details are only revealed after a submission.
