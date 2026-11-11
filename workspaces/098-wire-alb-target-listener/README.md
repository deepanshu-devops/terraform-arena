# 098 - Wire an ALB to a Target Group

**Level:** Level 4 - Composition  
**Difficulty:** Medium  
**Points:** 120  
**Tags:** aws, alb, load-balancing

## Scenario

Put an application load balancer in front of a target group and forward HTTP/80 traffic to it.

## What to complete

- File: `main.tf`
- Task: Complete the aws_lb_listener resource
- Add the arguments and nested blocks required for aws_lb_listener.

## Constraints

- ALB is application type and spans var.subnet_ids.
- Target group listens on HTTP/80.
- Listener forwards to the target group.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `subnet_ids` | `list(string)` | `required` |
| `security_group_ids` | `list(string)` | `required` |
| `vpc_id` | `string` | `required` |
| `project_name` | `string` | `terraform-practice` |
| `environment` | `string` | `dev` |
| `aws_region` | `string` | `us-east-1` |

## Expected resources

- `aws_lb`
- `aws_lb_target_group`
- `aws_lb_listener`

## Expected outputs

- `alb_dns_name`
- `target_group_arn`

## How to test

```powershell
python judge.py test 98 --dir workspaces/098-wire-alb-target-listener
```

> Hidden test details are only revealed after a submission.
