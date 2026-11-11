# 039 - Provision ACM Certificate

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

## Hints

**Why it matters:** `aws_acm_certificate` is a real building block in production configurations. The exercise isolates one decision so you can recognise the same shape when it appears inside a larger module.

**What to do:** Complete the marked region in `main.tf`. The work is inside `resource "aws_acm_certificate" "this"`. Add the arguments and nested blocks required for aws_acm_certificate. Use the visible constraints as the checklist for names, values and references before you run the tests.

**When to use it:** Use this pattern when the requirement is part of a reusable configuration that another person or environment must be able to reproduce.

**How to approach it:** Open `main.tf` and work only inside `resource "aws_acm_certificate" "this"`. Use this code shape: domain_name; tags; validation_method. Use the already-declared references instead of hardcoded values: `var.domain_name`, `var.project_name`, `var.environment`. Keep the block header and braces, indent nested blocks by two spaces, and add one argument or nested block at a time. Run the tests after each small change so the first failure points at the next name to fix.


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
python judge.py test 39 --dir workspaces/039-provision-acm-certificate
```

> Hidden test details are only revealed after a submission.
