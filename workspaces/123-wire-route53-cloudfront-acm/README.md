# 123 - Route 53 + ACM + CloudFront

**Level:** Level 4 - Composition  
**Difficulty:** Hard  
**Points:** 150  
**Tags:** aws, route53, cloudfront, acm, dns

## Scenario

Serve a domain through CloudFront with a DNS-validated certificate and an alias record.

## What to complete

- File: `main.tf`
- Task: Complete the aws_cloudfront_distribution resource
- Add the arguments and nested blocks required for aws_cloudfront_distribution.

## Hints

**Why it matters:** DNS is the public name of the system. Managing records in Terraform keeps the name, certificate and endpoint changes together.

**What to do:** Complete the marked region in `main.tf`. The work is inside `resource "aws_cloudfront_distribution" "this"`. Add the arguments and nested blocks required for aws_cloudfront_distribution. Use the visible constraints as the checklist for names, values and references before you run the tests.

**When to use it:** Use Route 53 when a service needs a stable hostname or when DNS changes should be reviewed with the rest of the stack.

**How to approach it:** Open `main.tf` and work only inside `resource "aws_cloudfront_distribution" "this"`. Use this code shape: enabled; default_cache_behavior { viewer_protocol_policy }; viewer_certificate { minimum_protocol_version; acm_certificate_arn; ssl_support_method }. Use the already-declared references instead of hardcoded values: `aws_acm_certificate.this.arn`. Keep the block header and braces, indent nested blocks by two spaces, and add one argument or nested block at a time. Run the tests after each small change so the first failure points at the next name to fix.


## Constraints

- Create a hosted zone, ACM certificate and CloudFront distribution.
- Create a Route 53 record in the zone.
- Certificate validation is DNS.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `domain_name` | `string` | `example.com` |
| `record_name` | `string` | `app` |
| `project_name` | `string` | `terraform-practice` |
| `environment` | `string` | `dev` |
| `aws_region` | `string` | `us-east-1` |

## Expected resources

- `aws_route53_zone`
- `aws_acm_certificate`
- `aws_cloudfront_distribution`
- `aws_route53_record`

## Expected outputs

- `zone_id`
- `certificate_arn`

## How to test

```powershell
python judge.py test 123 --dir workspaces/123-wire-route53-cloudfront-acm
```

> Hidden test details are only revealed after a submission.
