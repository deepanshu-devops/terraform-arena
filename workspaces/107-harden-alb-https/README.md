# 107 - ALB HTTPS Listener + Redirect

**Level:** Level 4 - Composition  
**Difficulty:** Hard  
**Points:** 130  
**Tags:** aws, alb, security, tls

## Scenario

Terminate TLS on the load balancer: an HTTPS listener on 443 with a certificate, and port 80 redirecting to HTTPS.

## What to complete

- File: `main.tf`
- Task: Complete the HTTPS listener
- Configure the 443/HTTPS listener with the certificate and a forward action.

## Constraints

- Two listeners: 443 HTTPS and 80 HTTP.
- 443 uses certificate_arn.
- 80 redirects to HTTPS.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `lb_arn` | `string` | `required` |
| `target_group_arn` | `string` | `required` |
| `certificate_arn` | `string` | `required` |

## Expected resources

- `aws_lb_listener`

## Expected outputs

- `listener_arn`

## How to test

```powershell
python judge.py test 107 --dir workspaces/107-harden-alb-https
```

> Hidden test details are only revealed after a submission.
