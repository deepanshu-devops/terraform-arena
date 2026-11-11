# 047 - Provision CloudFront Distribution

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

## Hints

**Why it matters:** A CDN changes latency, caching and the public attack surface. Origin and cache settings are part of the application contract.

**What to do:** Complete the marked TODO in `main.tf`. Add the arguments and nested blocks required for aws_cloudfront_distribution. Use the visible constraints as your checklist before you run the tests.

**When to use it:** Use CloudFront when content is served globally or when you need TLS, caching and origin protection in front of HTTP services.

**How to approach it:** Open `main.tf` and work inside the single TODO region. Change one requirement at a time: add the named block, argument or reference, then run the tests. When a check fails, match its wording to the constraints and fix only the block it names.


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
python judge.py test 47 --dir workspaces/047-provision-cloudfront
```

> Hidden test details are only revealed after a submission.
