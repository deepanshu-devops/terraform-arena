# 101 - CloudFront HTTPS-Only Distribution

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
python judge.py test 101 --dir workspaces/101-harden-cloudfront-https
```

> Hidden test details are only revealed after a submission.
