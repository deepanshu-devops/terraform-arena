# 049 - Provision CloudWatch Log Group

**Level:** Level 2 - First Resources  
**Difficulty:** Easy  
**Points:** 50  
**Tags:** aws, cloudwatch, provisioning

## Scenario

Your platform team needs CloudWatch Log Group for centralized application logs with retention. Write a reusable Terraform configuration that provisions it, drives every input through variables, applies the standard tags, and exports the operational identifiers.

## What to complete

- File: `main.tf`
- Task: Complete the aws_cloudwatch_log_group resource
- Add the arguments and nested blocks required for aws_cloudwatch_log_group.

## Hints

**Why it matters:** Observability resources turn an invisible system into something you can alert on. Metrics, logs and alarms belong with the infrastructure they monitor.

**What to do:** Complete the marked region in `main.tf`. The work is inside `resource "aws_cloudwatch_log_group" "this"`. Add the arguments and nested blocks required for aws_cloudwatch_log_group. Use the visible constraints as the checklist for names, values and references before you run the tests.

**When to use it:** Add monitoring whenever a resource has a failure mode that an operator must notice quickly.

**How to approach it:** Open `main.tf` and work only inside `resource "aws_cloudwatch_log_group" "this"`. Use this code shape: name; retention_in_days; tags. Use the already-declared references instead of hardcoded values: `var.log_group_name`, `var.project_name`, `var.environment`. Keep the block header and braces, indent nested blocks by two spaces, and add one argument or nested block at a time. Run the tests after each small change so the first failure points at the next name to fix.


## Constraints

- Provider: aws (region from var.aws_region).
- Create exactly one resource of type aws_cloudwatch_log_group.
- All configurable values must come from variables declared in variables.tf.
- No hardcoded AWS credentials.
- Code must pass terraform fmt conventions (2-space indents, trailing newline, no tabs).
- Tag the resource with Project, Environment and ManagedBy = "terraform".
- Expose outputs: log_group_arn.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `log_group_name` | `string` | `/app/logs` |
| `environment` | `string` | `dev` |
| `project_name` | `string` | `terraform-practice` |
| `aws_region` | `string` | `us-east-1` |

## Expected resources

- `aws_cloudwatch_log_group`

## Expected outputs

- `log_group_arn`

## How to test

```powershell
python judge.py test 49 --dir workspaces/049-provision-log-group
```

> Hidden test details are only revealed after a submission.
