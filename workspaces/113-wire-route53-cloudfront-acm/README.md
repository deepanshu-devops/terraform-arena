# 113 - Route 53 + ACM + CloudFront

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
python judge.py test 113 --dir workspaces/113-wire-route53-cloudfront-acm
```

> Hidden test details are only revealed after a submission.
