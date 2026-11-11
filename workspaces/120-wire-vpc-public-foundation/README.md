# 120 - Build a Public VPC Foundation

**Level:** Level 4 - Composition  
**Difficulty:** Medium  
**Points:** 140  
**Tags:** aws, vpc, networking

## Scenario

Assemble a minimal public VPC: VPC, public subnet, internet gateway, route table with a default route, and an association.

## What to complete

- File: `main.tf`
- Task: Complete the aws_subnet resource
- Add the arguments and nested blocks required for aws_subnet.

## Hints

**Why it matters:** A VPC is the network boundary for most AWS resources. CIDR planning, subnets and routing decisions affect everything deployed inside it.

**What to do:** Complete the marked TODO in `main.tf`. Add the arguments and nested blocks required for aws_subnet. Use the visible constraints as your checklist before you run the tests.

**When to use it:** Design a VPC when you need isolated networking, predictable address space or control over public and private traffic.

**How to approach it:** Open `main.tf` and work inside the single TODO region. Change one requirement at a time: add the named block, argument or reference, then run the tests. When a check fails, match its wording to the constraints and fix only the block it names.


## Constraints

- One VPC, one public subnet, one IGW, one route table and one association.
- Default route 0.0.0.0/0 -> IGW.
- Tag core resources.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `vpc_cidr` | `string` | `10.0.0.0/16` |
| `subnet_cidr` | `string` | `10.0.1.0/24` |
| `availability_zone` | `string` | `us-east-1a` |
| `project_name` | `string` | `terraform-practice` |
| `environment` | `string` | `dev` |
| `aws_region` | `string` | `us-east-1` |

## Expected resources

- `aws_vpc`
- `aws_subnet`
- `aws_internet_gateway`
- `aws_route_table`
- `aws_route`
- `aws_route_table_association`

## Expected outputs

- `vpc_id`
- `subnet_id`
- `internet_gateway_id`

## How to test

```powershell
python judge.py test 120 --dir workspaces/120-wire-vpc-public-foundation
```

> Hidden test details are only revealed after a submission.
