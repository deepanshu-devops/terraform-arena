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

**What to do:** Complete the marked region in `main.tf`. The work is inside `resource "aws_flow_log" "this"`. Add the arguments and nested blocks required for aws_flow_log. Use the visible constraints as the checklist for names, values and references before you run the tests.

**When to use it:** Design a VPC when you need isolated networking, predictable address space or control over public and private traffic.

**How to approach it:** Open `main.tf` and work only inside `resource "aws_flow_log" "this"`. Use this code shape: traffic_type; log_destination; log_destination_type. Use the already-declared references instead of hardcoded values: `aws_cloudwatch_log_group.this.arn`. Keep the block header and braces, indent nested blocks by two spaces, and add one argument or nested block at a time. Run the tests after each small change so the first failure points at the next name to fix.


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
