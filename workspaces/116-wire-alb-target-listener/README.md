# 116 - Wire an ALB to a Target Group

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

## Hints

**Why it matters:** A load balancer is the stable entry point in front of changing compute. Listeners and target groups define how traffic reaches the application.

**What to do:** Complete the marked region in `main.tf`. The work is inside `resource "aws_lb_listener" "this"`. Add the arguments and nested blocks required for aws_lb_listener. Use the visible constraints as the checklist for names, values and references before you run the tests.

**When to use it:** Use a load balancer when traffic must be distributed, health-checked or terminated before reaching backend instances.

**How to approach it:** Open `main.tf` and work only inside `resource "aws_lb_listener" "this"`. Use this code shape: port; protocol; load_balancer_arn; default_action { type; target_group_arn }. Use the already-declared references instead of hardcoded values: `aws_lb.this.arn`, `aws_lb_target_group.this.arn`. Keep the block header and braces, indent nested blocks by two spaces, and add one argument or nested block at a time. Run the tests after each small change so the first failure points at the next name to fix.


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
python judge.py test 116 --dir workspaces/116-wire-alb-target-listener
```

> Hidden test details are only revealed after a submission.
