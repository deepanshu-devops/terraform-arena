# 024 - Create Subnets With count

**Level:** Level 1 - Terraform Language  
**Difficulty:** Medium  
**Points:** 90  
**Tags:** terraform, count, networking

## Scenario

Create two public subnets using a single aws_subnet resource with count and count.index.

## What to complete

- File: `main.tf`
- Task: Complete the aws_subnet block
- Use count and the subnet CIDR list so one subnet is created per entry.

## Constraints

- Use count = 2 or length(var.subnet_cidrs).
- Reference count.index for the CIDR/AZ.
- One resource block, not two.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `vpc_id` | `string` | `required` |
| `subnet_cidrs` | `list(string)` | `['10.0.1.0/24', '10.0.2.0/24']` |
| `availability_zones` | `list(string)` | `['us-east-1a', 'us-east-1b']` |

## Expected resources

- `aws_subnet`

## Expected outputs

- `subnet_ids`

## How to test

```powershell
python judge.py test 24 --dir workspaces/024-lang-count-subnets
```

> Hidden test details are only revealed after a submission.
