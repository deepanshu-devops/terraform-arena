# 041 - Provision ALB Target Group

**Level:** Level 2 - First Resources  
**Difficulty:** Easy  
**Points:** 50  
**Tags:** aws, alb, provisioning

## Scenario

Your platform team needs ALB Target Group for health-checked backend targets. Write a reusable Terraform configuration that provisions it, drives every input through variables, applies the standard tags, and exports the operational identifiers.

## What to complete

- File: `main.tf`
- Task: Complete the aws_lb_target_group resource
- Add the arguments and nested blocks required for aws_lb_target_group.

## Hints

**Why it matters:** A load balancer is the stable entry point in front of changing compute. Listeners and target groups define how traffic reaches the application.

**What to do:** Complete the marked region in `main.tf`. The work is inside `resource "aws_lb_target_group" "this"`. Add the arguments and nested blocks required for aws_lb_target_group. Use the visible constraints as the checklist for names, values and references before you run the tests.

**When to use it:** Use a load balancer when traffic must be distributed, health-checked or terminated before reaching backend instances.

**How to approach it:** Open `main.tf` and work only inside `resource "aws_lb_target_group" "this"`. Use this code shape: name; port; protocol; tags; vpc_id; health_check { path }. Use the already-declared references instead of hardcoded values: `var.project_name`, `var.environment`, `var.vpc_id`. Keep the block header and braces, indent nested blocks by two spaces, and add one argument or nested block at a time. Run the tests after each small change so the first failure points at the next name to fix.


## Constraints

- Provider: aws (region from var.aws_region).
- Create exactly one resource of type aws_lb_target_group.
- All configurable values must come from variables declared in variables.tf.
- No hardcoded AWS credentials.
- Code must pass terraform fmt conventions (2-space indents, trailing newline, no tabs).
- Tag the resource with Project, Environment and ManagedBy = "terraform".
- Expose outputs: target_group_arn.
- Allowed supporting resources: aws_vpc.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `vpc_id` | `string` | `required` |
| `environment` | `string` | `dev` |
| `project_name` | `string` | `terraform-practice` |
| `aws_region` | `string` | `us-east-1` |

## Expected resources

- `aws_lb_target_group`

## Expected outputs

- `target_group_arn`

## How to test

```powershell
python judge.py test 41 --dir workspaces/041-provision-target-group
```

> Hidden test details are only revealed after a submission.
