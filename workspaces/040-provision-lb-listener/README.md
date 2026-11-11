# 040 - Provision ALB Listener

**Level:** Level 2 - First Resources  
**Difficulty:** Easy  
**Points:** 50  
**Tags:** aws, alb, provisioning

## Scenario

Your platform team needs ALB Listener for accepting HTTP traffic on port 80. Write a reusable Terraform configuration that provisions it, drives every input through variables, applies the standard tags, and exports the operational identifiers.

## What to complete

- File: `main.tf`
- Task: Complete the aws_lb_listener resource
- Add the arguments and nested blocks required for aws_lb_listener.

## Hints

**Why it matters:** A load balancer is the stable entry point in front of changing compute. Listeners and target groups define how traffic reaches the application.

**What to do:** Complete the marked region in `main.tf`. The work is inside `resource "aws_lb_listener" "this"`. Add the arguments and nested blocks required for aws_lb_listener. Use the visible constraints as the checklist for names, values and references before you run the tests.

**When to use it:** Use a load balancer when traffic must be distributed, health-checked or terminated before reaching backend instances.

**How to approach it:** Open `main.tf` and work only inside `resource "aws_lb_listener" "this"`. Use this code shape: port; protocol; load_balancer_arn; default_action { type; target_group_arn }. Use the already-declared references instead of hardcoded values: `var.lb_arn`, `aws_lb_target_group.this.arn`. Keep the block header and braces, indent nested blocks by two spaces, and add one argument or nested block at a time. Run the tests after each small change so the first failure points at the next name to fix.


## Constraints

- Provider: aws (region from var.aws_region).
- Create exactly one resource of type aws_lb_listener.
- All configurable values must come from variables declared in variables.tf.
- No hardcoded AWS credentials.
- Code must pass terraform fmt conventions (2-space indents, trailing newline, no tabs).
- Expose outputs: listener_arn.
- Allowed supporting resources: aws_lb, aws_lb_target_group.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `lb_arn` | `string` | `required` |
| `target_group_arn` | `string` | `required` |
| `aws_region` | `string` | `us-east-1` |

## Expected resources

- `aws_lb_listener`

## Expected outputs

- `listener_arn`

## How to test

```powershell
python judge.py test 40 --dir workspaces/040-provision-lb-listener
```

> Hidden test details are only revealed after a submission.
