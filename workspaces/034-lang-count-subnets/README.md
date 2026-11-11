# 034 - Create Subnets With count

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

## Hints

**Why it matters:** count is the simplest way to create a repeated resource from a collection. It teaches how Terraform addresses instances and why changing list order can be risky.

**What to do:** Complete the marked TODO in `main.tf`. Use count and the subnet CIDR list so one subnet is created per entry. Use the visible constraints as your checklist before you run the tests.

**When to use it:** Use count when instances are interchangeable and their position is stable. Prefer for_each when each instance has a meaningful name.

**How to approach it:** Open `main.tf` and work inside the single TODO region. Change one requirement at a time: add the named block, argument or reference, then run the tests. When a check fails, match its wording to the constraints and fix only the block it names.


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
python judge.py test 34 --dir workspaces/034-lang-count-subnets
```

> Hidden test details are only revealed after a submission.
