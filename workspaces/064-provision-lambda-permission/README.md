# 064 - Provision Lambda Invoke Permission

**Level:** Level 2 - First Resources  
**Difficulty:** Easy  
**Points:** 50  
**Tags:** aws, lambda, provisioning

## Scenario

Your platform team needs Lambda Invoke Permission for allowing API Gateway to invoke a function. Write a reusable Terraform configuration that provisions it, drives every input through variables, applies the standard tags, and exports the operational identifiers.

## What to complete

- File: `main.tf`
- Task: Complete the aws_lambda_permission resource
- Add the arguments and nested blocks required for aws_lambda_permission.

## Hints

**Why it matters:** Lambda packages compute as a small, event-driven unit. The code artifact, execution role and trigger are the contract to get right.

**What to do:** Complete the marked region in `main.tf`. The work is inside `resource "aws_lambda_permission" "this"`. Add the arguments and nested blocks required for aws_lambda_permission. Use the visible constraints as the checklist for names, values and references before you run the tests.

**When to use it:** Use Lambda for short-lived event handlers or glue code where managing a server would add cost and operational noise.

**How to approach it:** Open `main.tf` and work only inside `resource "aws_lambda_permission" "this"`. Use this code shape: statement_id; action; function_name; principal. Use the already-declared references instead of hardcoded values: `var.lambda_function_name`. Keep the block header and braces, indent nested blocks by two spaces, and add one argument or nested block at a time. Run the tests after each small change so the first failure points at the next name to fix.


## Constraints

- Provider: aws (region from var.aws_region).
- Create exactly one resource of type aws_lambda_permission.
- All configurable values must come from variables declared in variables.tf.
- No hardcoded AWS credentials.
- Code must pass terraform fmt conventions (2-space indents, trailing newline, no tabs).
- Expose outputs: statement_id.
- Allowed supporting resources: aws_lambda_function.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `lambda_function_name` | `string` | `required` |
| `aws_region` | `string` | `us-east-1` |

## Expected resources

- `aws_lambda_permission`

## Expected outputs

- `statement_id`

## How to test

```powershell
python judge.py test 64 --dir workspaces/064-provision-lambda-permission
```

> Hidden test details are only revealed after a submission.
