# 074 - Provision Step Functions State Machine

**Level:** Level 3 - Real Infrastructure  
**Difficulty:** Medium  
**Points:** 80  
**Tags:** aws, step-functions, provisioning

## Scenario

Your platform team needs Step Functions State Machine for an orchestration workflow for async jobs. Write a reusable Terraform configuration that provisions it, drives every input through variables, applies the standard tags, and exports the operational identifiers.

## What to complete

- File: `main.tf`
- Task: Complete the aws_stepfunctions_state_machine resource
- Add the arguments and nested blocks required for aws_stepfunctions_state_machine.

## Constraints

- Provider: aws (region from var.aws_region).
- Create exactly one resource of type aws_stepfunctions_state_machine.
- All configurable values must come from variables declared in variables.tf.
- No hardcoded AWS credentials.
- Code must pass terraform fmt conventions (2-space indents, trailing newline, no tabs).
- Tag the resource with Project, Environment and ManagedBy = "terraform".
- Expose outputs: state_machine_arn.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `state_machine_name` | `string` | `order-flow` |
| `role_arn` | `string` | `required` |
| `environment` | `string` | `dev` |
| `project_name` | `string` | `terraform-practice` |
| `aws_region` | `string` | `us-east-1` |

## Expected resources

- `aws_stepfunctions_state_machine`

## Expected outputs

- `state_machine_arn`

## How to test

```powershell
python judge.py test 74 --dir workspaces/074-provision-stepfunctions
```

> Hidden test details are only revealed after a submission.
