# 101 - Security Group Without Public SSH

**Level:** Level 3 - Real Infrastructure  
**Difficulty:** Medium  
**Points:** 90  
**Tags:** aws, ec2, security, networking

## Scenario

Lock down a security group: allow HTTPS from the internet, never SSH from 0.0.0.0/0.

## What to complete

- File: `main.tf`
- Task: Complete the aws_security_group resource
- Add the arguments and nested blocks required for aws_security_group.

## Hints

**Why it matters:** EC2 teaches the core lifecycle of compute: image, instance type, networking, storage and safe replacement.

**What to do:** Complete the marked region in `main.tf`. The work is inside `resource "aws_security_group" "this"`. Add the arguments and nested blocks required for aws_security_group. Use the visible constraints as the checklist for names, values and references before you run the tests.

**When to use it:** Use EC2 when you need a virtual machine you control directly, or as a building block inside an autoscaling or container platform.

**How to approach it:** Open `main.tf` and work only inside `resource "aws_security_group" "this"`. Use this code shape: name; description; vpc_id; ingress { from_port; to_port; protocol; cidr_blocks }; ingress {}; egress { from_port; to_port; protocol; cidr_blocks }. Use the already-declared references instead of hardcoded values: `var.vpc_id`. Keep the block header and braces, indent nested blocks by two spaces, and add one argument or nested block at a time. Run the tests after each small change so the first failure points at the next name to fix.


## Constraints

- Allow port 443 ingress.
- No ingress on port 22 from 0.0.0.0/0.
- Belongs to var.vpc_id.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `vpc_id` | `string` | `required` |
| `security_group_name` | `string` | `web-sg` |

## Expected resources

- `aws_security_group`

## Expected outputs

- `security_group_id`

## How to test

```powershell
python judge.py test 101 --dir workspaces/101-harden-sg-no-ssh
```

> Hidden test details are only revealed after a submission.
