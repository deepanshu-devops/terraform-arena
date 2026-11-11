# 111 - CloudFront HTTPS-Only Distribution

**Level:** Level 4 - Composition  
**Difficulty:** Hard  
**Points:** 120  
**Tags:** aws, cloudfront, security, tls

## Scenario

Serve a CDN distribution that redirects viewers to HTTPS and requires a modern TLS policy.

## What to complete

- File: `main.tf`
- Task: Complete the aws_cloudfront_distribution resource
- Add the arguments and nested blocks required for aws_cloudfront_distribution.

## Hints

**Why it matters:** A CDN changes latency, caching and the public attack surface. Origin and cache settings are part of the application contract.

**What to do:** Complete the marked region in `main.tf`. The work is inside `resource "aws_cloudfront_distribution" "this"`. Add the arguments and nested blocks required for aws_cloudfront_distribution. Use the visible constraints as the checklist for names, values and references before you run the tests.

**When to use it:** Use CloudFront when content is served globally or when you need TLS, caching and origin protection in front of HTTP services.

**How to approach it:** Open `main.tf` and work only inside `resource "aws_cloudfront_distribution" "this"`. Use this code shape: enabled; default_cache_behavior { viewer_protocol_policy }; viewer_certificate { minimum_protocol_version }. Keep the block header and braces, indent nested blocks by two spaces, and add one argument or nested block at a time. Run the tests after each small change so the first failure points at the next name to fix.


## Constraints

- enabled = true.
- viewer_protocol_policy = redirect-to-https.
- minimum_protocol_version = TLSv1.2_2021.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `origin_domain_name` | `string` | `example.com` |
| `certificate_arn` | `string` | `required` |

## Expected resources

- `aws_cloudfront_distribution`

## Expected outputs

- `domain_name`

## How to test

```powershell
python judge.py test 111 --dir workspaces/111-harden-cloudfront-https
```

> Hidden test details are only revealed after a submission.
