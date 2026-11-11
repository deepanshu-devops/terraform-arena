# 103 - SQS Queue With Dead-Letter Queue

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

## Hints

**Why it matters:** Queues decouple producers from consumers and absorb bursts. Visibility timeouts and retention settings are part of the reliability contract.

**What to do:** Complete the marked region in `main.tf`. The work is inside `resource "aws_sqs_queue" "this"`. Add the queue name, server-side encryption and redrive policy pointing at the DLQ. Use the visible constraints as the checklist for names, values and references before you run the tests.

**When to use it:** Use a queue when work can be processed asynchronously or when two components should not fail together.

**How to approach it:** Open `main.tf` and work only inside `resource "aws_sqs_queue" "this"`. Use this code shape: name; sqs_managed_sse_enabled; redrive_policy. Use the already-declared references instead of hardcoded values: `var.queue_name`, `aws_sqs_queue.dlq.arn`. Keep the block header and braces, indent nested blocks by two spaces, and add one argument or nested block at a time. Run the tests after each small change so the first failure points at the next name to fix.


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
python judge.py test 103 --dir workspaces/103-harden-sqs-dlq
```

> Hidden test details are only revealed after a submission.
