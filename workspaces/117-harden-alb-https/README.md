# 117 - ALB HTTPS Listener + Redirect

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

## Hints

**Why it matters:** A load balancer is the stable entry point in front of changing compute. Listeners and target groups define how traffic reaches the application.

**What to do:** Complete the marked TODO in `main.tf`. Configure the 443/HTTPS listener with the certificate and a forward action. Use the visible constraints as your checklist before you run the tests.

**When to use it:** Use a load balancer when traffic must be distributed, health-checked or terminated before reaching backend instances.

**How to approach it:** Open `main.tf` and work inside the single TODO region. Change one requirement at a time: add the named block, argument or reference, then run the tests. When a check fails, match its wording to the constraints and fix only the block it names.


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
python judge.py test 117 --dir workspaces/117-harden-alb-https
```

> Hidden test details are only revealed after a submission.
