# 097 - Fan Out SNS to SQS

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
python judge.py test 97 --dir workspaces/097-wire-sqs-sns
```

> Hidden test details are only revealed after a submission.
