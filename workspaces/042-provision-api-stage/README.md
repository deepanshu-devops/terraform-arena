# 042 - Provision API Gateway Stage

**Level:** Level 2 - First Resources  
**Difficulty:** Easy  
**Points:** 50  
**Tags:** aws, api-gateway, provisioning

## Scenario

Your platform team needs API Gateway Stage for a deployed stage for an HTTP API. Write a reusable Terraform configuration that provisions it, drives every input through variables, applies the standard tags, and exports the operational identifiers.

## What to complete

- File: `main.tf`
- Task: Complete the aws_apigatewayv2_stage resource
- Add the arguments and nested blocks required for aws_apigatewayv2_stage.

## Hints

**Why it matters:** API Gateway is the front door for HTTP APIs. Routes, stages and integrations decide how requests reach backend compute.

**What to do:** Complete the marked TODO in `main.tf`. Add the arguments and nested blocks required for aws_apigatewayv2_stage. Use the visible constraints as your checklist before you run the tests.

**When to use it:** Use an API gateway when you need a managed public API surface, throttling or request routing.

**How to approach it:** Open `main.tf` and work inside the single TODO region. Change one requirement at a time: add the named block, argument or reference, then run the tests. When a check fails, match its wording to the constraints and fix only the block it names.


## Constraints

- Provider: aws (region from var.aws_region).
- Create exactly one resource of type aws_apigatewayv2_stage.
- All configurable values must come from variables declared in variables.tf.
- No hardcoded AWS credentials.
- Code must pass terraform fmt conventions (2-space indents, trailing newline, no tabs).
- Tag the resource with Project, Environment and ManagedBy = "terraform".
- Expose outputs: invoke_url.
- Allowed supporting resources: aws_apigatewayv2_api.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `api_id` | `string` | `required` |
| `stage_name` | `string` | `prod` |
| `environment` | `string` | `dev` |
| `project_name` | `string` | `terraform-practice` |
| `aws_region` | `string` | `us-east-1` |

## Expected resources

- `aws_apigatewayv2_stage`

## Expected outputs

- `invoke_url`

## How to test

```powershell
python judge.py test 42 --dir workspaces/042-provision-api-stage
```

> Hidden test details are only revealed after a submission.
