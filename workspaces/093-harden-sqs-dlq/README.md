# 093 - SQS Queue With Dead-Letter Queue

**Level:** Level 3 - Real Infrastructure  
**Difficulty:** Medium  
**Points:** 100  
**Tags:** aws, sqs, resilience

## Scenario

Build a durable queue with a dead-letter queue for poison messages and server-side encryption.

## What to complete

- File: `main.tf`
- Task: Complete the main queue
- Add the queue name, server-side encryption and redrive policy pointing at the DLQ.

## Constraints

- Create a main queue and a DLQ.
- Main queue redrive_policy points at the DLQ.
- sqs_managed_sse_enabled = true.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `queue_name` | `string` | `jobs` |
| `dlq_name` | `string` | `jobs-dlq` |

## Expected resources

- `aws_sqs_queue`

## Expected outputs

- `queue_url`

## How to test

```powershell
python judge.py test 93 --dir workspaces/093-harden-sqs-dlq
```

> Hidden test details are only revealed after a submission.
