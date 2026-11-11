# 107 - Fan Out SNS to SQS

**Level:** Level 4 - Composition  
**Difficulty:** Medium  
**Points:** 100  
**Tags:** aws, sns, sqs, messaging

## Scenario

Publish events to an SNS topic and deliver them to an encrypted SQS queue through a subscription.

## What to complete

- File: `main.tf`
- Task: Complete the aws_sns_topic_subscription resource
- Add the arguments and nested blocks required for aws_sns_topic_subscription.

## Hints

**Why it matters:** Topics provide fan-out messaging. Subscriptions decide who receives events and in what format.

**What to do:** Complete the marked region in `main.tf`. The work is inside `resource "aws_sns_topic_subscription" "this"`. Add the arguments and nested blocks required for aws_sns_topic_subscription. Use the visible constraints as the checklist for names, values and references before you run the tests.

**When to use it:** Use SNS when one event should notify several consumers or when you need a simple pub/sub boundary.

**How to approach it:** Open `main.tf` and work only inside `resource "aws_sns_topic_subscription" "this"`. Use this code shape: protocol; topic_arn; endpoint. Use the already-declared references instead of hardcoded values: `aws_sns_topic.this.arn`, `aws_sqs_queue.this.arn`. Keep the block header and braces, indent nested blocks by two spaces, and add one argument or nested block at a time. Run the tests after each small change so the first failure points at the next name to fix.


## Constraints

- Create topic, queue and subscription.
- Subscription protocol is sqs.
- Queue uses managed SSE.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `topic_name` | `string` | `events` |
| `queue_name` | `string` | `events-queue` |
| `project_name` | `string` | `terraform-practice` |
| `environment` | `string` | `dev` |
| `aws_region` | `string` | `us-east-1` |

## Expected resources

- `aws_sns_topic`
- `aws_sqs_queue`
- `aws_sns_topic_subscription`

## Expected outputs

- `topic_arn`
- `queue_url`

## How to test

```powershell
python judge.py test 107 --dir workspaces/107-wire-sqs-sns
```

> Hidden test details are only revealed after a submission.
