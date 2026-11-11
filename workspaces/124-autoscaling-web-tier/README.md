# 124 - Auto Scaling Web Tier

**Level:** Level 5 - Modules & Capstones  
**Difficulty:** Hard  
**Points:** 250  
**Tags:** aws, alb, autoscaling, launch-template, security

## Scenario

Expose a stateless web tier behind an Application Load Balancer. The fleet must be built from a hardened launch template (IMDSv2 enforced), scale between configurable bounds across the provided subnets, and register automatically with an ALB target group. This is the production-shaped version of the classic 'web app on EC2' task.

## What to complete

- File: `main.tf`
- Task: Complete the Auto Scaling group
- Wire the size variables, subnets, target group, launch template and propagated tags.

## Constraints

- Provider: AWS with region from var.aws_region.
- Discover the Amazon Linux AMI through a data.aws_ami source (do not hardcode an AMI id).
- instance_type defaults to t2.micro and is validated against a free-tier allowlist.
- asg_min / asg_max / asg_desired are number variables; asg_max must be capped (<= 4).
- vpc_id (string) and subnet_ids (list(string)) are required inputs — no defaults.
- Security group must allow HTTP/80 from 0.0.0.0/0 and must not expose SSH/22 to the world.
- Launch template must enforce IMDSv2 (metadata_options.http_tokens = required) and tag instances.
- ALB must be application type, span var.subnet_ids and use the security group.
- Target group on HTTP/80 with a health check path from var.health_check_path.
- Listener forwards port 80 to the target group.
- ASG uses the size variables, spans var.subnet_ids, registers with the target group and uses ELB health checks.
- Outputs: alb_dns_name, asg_name, security_group_id.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `vpc_id` | `string` | `None` |
| `subnet_ids` | `list(string)` | `None` |
| `instance_type` | `string` | `t2.micro` |
| `asg_min` | `number` | `1` |
| `asg_max` | `number` | `2` |
| `asg_desired` | `number` | `1` |
| `health_check_path` | `string` | `/` |
| `aws_region` | `string` | `us-east-1` |
| `project_name` | `string` | `terraform-practice` |
| `environment` | `string` | `dev` |

## Expected resources

- `aws_security_group`
- `aws_launch_template`
- `aws_lb`
- `aws_lb_target_group`
- `aws_lb_listener`
- `aws_autoscaling_group`

## Expected outputs

- `alb_dns_name`
- `asg_name`
- `security_group_id`

## How to test

```powershell
python judge.py test 124 --dir workspaces/124-autoscaling-web-tier
```

> Hidden test details are only revealed after a submission.
