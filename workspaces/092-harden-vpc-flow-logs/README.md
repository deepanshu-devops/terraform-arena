# 092 - Enable VPC Flow Logs

**Level:** Level 3 - Real Infrastructure  
**Difficulty:** Medium  
**Points:** 100  
**Tags:** aws, vpc, observability, security

## Scenario

Send ALL VPC traffic to CloudWatch Logs so the security team can investigate anomalies.

## What to complete

- File: `main.tf`
- Task: Complete the aws_flow_log resource
- Add the arguments and nested blocks required for aws_flow_log.

## Constraints

- Create a CloudWatch log group and a flow log.
- traffic_type = ALL.
- Flow log targets the VPC.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `vpc_id` | `string` | `required` |

## Expected resources

- `aws_vpc`
- `aws_cloudwatch_log_group`
- `aws_flow_log`

## Expected outputs

- `flow_log_id`

## How to test

```powershell
python judge.py test 92 --dir workspaces/092-harden-vpc-flow-logs
```

> Hidden test details are only revealed after a submission.
