# 030 - Provision ALB Listener

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
python judge.py test 30 --dir workspaces/030-provision-lb-listener
```

> Hidden test details are only revealed after a submission.
