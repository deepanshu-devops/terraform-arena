# 102 - Enable VPC Flow Logs

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

## Hints

**Why it matters:** A VPC is the network boundary for most AWS resources. CIDR planning, subnets and routing decisions affect everything deployed inside it.

**What to do:** Complete the marked TODO in `main.tf`. Add the arguments and nested blocks required for aws_flow_log. Use the visible constraints as your checklist before you run the tests.

**When to use it:** Design a VPC when you need isolated networking, predictable address space or control over public and private traffic.

**How to approach it:** Open `main.tf` and work inside the single TODO region. Change one requirement at a time: add the named block, argument or reference, then run the tests. When a check fails, match its wording to the constraints and fix only the block it names.


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
python judge.py test 102 --dir workspaces/102-harden-vpc-flow-logs
```

> Hidden test details are only revealed after a submission.
