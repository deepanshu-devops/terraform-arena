# 069 - Provision SQS Queue

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
python judge.py test 69 --dir workspaces/069-provision-sqs-queue
```

> Hidden test details are only revealed after a submission.
