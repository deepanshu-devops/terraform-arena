# 092 - Provision Step Functions State Machine

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

## Hints

**Why it matters:** `aws_stepfunctions_state_machine` is a real building block in production configurations. The exercise isolates one decision so you can recognise the same shape when it appears inside a larger module.

**What to do:** Complete the marked region in `main.tf`. The work is inside `resource "aws_stepfunctions_state_machine" "this"`. Add the arguments and nested blocks required for aws_stepfunctions_state_machine. Use the visible constraints as the checklist for names, values and references before you run the tests.

**When to use it:** Use this pattern when the requirement is part of a reusable configuration that another person or environment must be able to reproduce.

**How to approach it:** Open `main.tf` and work only inside `resource "aws_stepfunctions_state_machine" "this"`. Use this code shape: name; definition; role_arn; tags. Use the already-declared references instead of hardcoded values: `var.state_machine_name`, `var.role_arn`, `var.project_name`, `var.environment`. Keep the block header and braces, indent nested blocks by two spaces, and add one argument or nested block at a time. Run the tests after each small change so the first failure points at the next name to fix.


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
python judge.py test 92 --dir workspaces/092-provision-stepfunctions
```

> Hidden test details are only revealed after a submission.
