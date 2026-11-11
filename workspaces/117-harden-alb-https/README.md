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

**What to do:** Complete the marked region in `main.tf`. The work is inside `resource "aws_lb_listener" "https"`. Configure the 443/HTTPS listener with the certificate and a forward action. Use the visible constraints as the checklist for names, values and references before you run the tests.

**When to use it:** Use a load balancer when traffic must be distributed, health-checked or terminated before reaching backend instances.

**How to approach it:** Open `main.tf` and work only inside `resource "aws_lb_listener" "https"`. Use this code shape: port; protocol; certificate_arn; load_balancer_arn; default_action { type; target_group_arn }. Use the already-declared references instead of hardcoded values: `var.certificate_arn`, `var.lb_arn`, `var.target_group_arn`. Keep the block header and braces, indent nested blocks by two spaces, and add one argument or nested block at a time. Run the tests after each small change so the first failure points at the next name to fix.


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
