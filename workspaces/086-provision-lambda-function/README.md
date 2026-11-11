# 086 - Provision Lambda Function

**Level:** Level 3 - Real Infrastructure  
**Difficulty:** Medium  
**Points:** 70  
**Tags:** aws, lambda, provisioning

## Scenario

Your platform team needs Lambda Function for an event-driven Python function. Write a reusable Terraform configuration that provisions it, drives every input through variables, applies the standard tags, and exports the operational identifiers.

## What to complete

- File: `main.tf`
- Task: Complete the aws_lambda_function resource
- Add the arguments and nested blocks required for aws_lambda_function.

## Hints

**Why it matters:** Lambda packages compute as a small, event-driven unit. The code artifact, execution role and trigger are the contract to get right.

**What to do:** Complete the marked region in `main.tf`. The work is inside `resource "aws_lambda_function" "this"`. Add the arguments and nested blocks required for aws_lambda_function. Use the visible constraints as the checklist for names, values and references before you run the tests.

**When to use it:** Use Lambda for short-lived event handlers or glue code where managing a server would add cost and operational noise.

**How to approach it:** Open `main.tf` and work only inside `resource "aws_lambda_function" "this"`. Use this code shape: function_name; runtime; handler; filename; memory_size; tags; role; environment { variables }. Use the already-declared references instead of hardcoded values: `var.lambda_runtime`, `var.lambda_memory`, `var.project_name`, `var.environment`, `var.lambda_role_arn`. Keep the block header and braces, indent nested blocks by two spaces, and add one argument or nested block at a time. Run the tests after each small change so the first failure points at the next name to fix.


## Constraints

- Provider: aws (region from var.aws_region).
- Create exactly one resource of type aws_lambda_function.
- All configurable values must come from variables declared in variables.tf.
- No hardcoded AWS credentials.
- Code must pass terraform fmt conventions (2-space indents, trailing newline, no tabs).
- Tag the resource with Project, Environment and ManagedBy = "terraform".
- Expose outputs: lambda_arn.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `lambda_role_arn` | `string` | `required` |
| `lambda_runtime` | `string` | `python3.12` |
| `lambda_memory` | `number` | `128` |
| `environment` | `string` | `dev` |
| `project_name` | `string` | `terraform-practice` |
| `aws_region` | `string` | `us-east-1` |

## Expected resources

- `aws_lambda_function`

## Expected outputs

- `lambda_arn`

## How to test

```powershell
python judge.py test 86 --dir workspaces/086-provision-lambda-function
```

> Hidden test details are only revealed after a submission.
