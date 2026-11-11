# 093 - Provision WAF Web ACL

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

## Hints

**Why it matters:** `aws_wafv2_web_acl` is a real building block in production configurations. The exercise isolates one decision so you can recognise the same shape when it appears inside a larger module.

**What to do:** Complete the marked region in `main.tf`. The work is inside `resource "aws_wafv2_web_acl" "this"`. Add the arguments and nested blocks required for aws_wafv2_web_acl. Use the visible constraints as the checklist for names, values and references before you run the tests.

**When to use it:** Use this pattern when the requirement is part of a reusable configuration that another person or environment must be able to reproduce.

**How to approach it:** Open `main.tf` and work only inside `resource "aws_wafv2_web_acl" "this"`. Use this code shape: name; scope; tags; default_action { allow {} }. Use the already-declared references instead of hardcoded values: `var.web_acl_name`, `var.project_name`, `var.environment`. Keep the block header and braces, indent nested blocks by two spaces, and add one argument or nested block at a time. Run the tests after each small change so the first failure points at the next name to fix.


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
python judge.py test 93 --dir workspaces/093-provision-waf-web-acl
```

> Hidden test details are only revealed after a submission.
