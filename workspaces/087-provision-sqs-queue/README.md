# 087 - Provision SQS Queue

**Level:** Level 3 - Real Infrastructure  
**Difficulty:** Medium  
**Points:** 70  
**Tags:** aws, sqs, provisioning

## Scenario

Your platform team needs SQS Queue for a durable work queue with encryption. Write a reusable Terraform configuration that provisions it, drives every input through variables, applies the standard tags, and exports the operational identifiers.

## What to complete

- File: `main.tf`
- Task: Complete the aws_sqs_queue resource
- Add the arguments and nested blocks required for aws_sqs_queue.

## Hints

**Why it matters:** Queues decouple producers from consumers and absorb bursts. Visibility timeouts and retention settings are part of the reliability contract.

**What to do:** Complete the marked region in `main.tf`. The work is inside `resource "aws_sqs_queue" "this"`. Add the arguments and nested blocks required for aws_sqs_queue. Use the visible constraints as the checklist for names, values and references before you run the tests.

**When to use it:** Use a queue when work can be processed asynchronously or when two components should not fail together.

**How to approach it:** Open `main.tf` and work only inside `resource "aws_sqs_queue" "this"`. Use this code shape: name; tags; sqs_managed_sse_enabled; message_retention_seconds. Use the already-declared references instead of hardcoded values: `var.queue_name`, `var.project_name`, `var.environment`. Keep the block header and braces, indent nested blocks by two spaces, and add one argument or nested block at a time. Run the tests after each small change so the first failure points at the next name to fix.


## Constraints

- Provider: aws (region from var.aws_region).
- Create exactly one resource of type aws_sqs_queue.
- All configurable values must come from variables declared in variables.tf.
- No hardcoded AWS credentials.
- Code must pass terraform fmt conventions (2-space indents, trailing newline, no tabs).
- Tag the resource with Project, Environment and ManagedBy = "terraform".
- Expose outputs: queue_url, queue_arn.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `queue_name` | `string` | `jobs` |
| `environment` | `string` | `dev` |
| `project_name` | `string` | `terraform-practice` |
| `aws_region` | `string` | `us-east-1` |

## Expected resources

- `aws_sqs_queue`

## Expected outputs

- `queue_url`
- `queue_arn`

## How to test

```powershell
python judge.py test 87 --dir workspaces/087-provision-sqs-queue
```

> Hidden test details are only revealed after a submission.
