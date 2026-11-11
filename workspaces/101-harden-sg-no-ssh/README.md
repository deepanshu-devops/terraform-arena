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

**What to do:** Complete the marked TODO in `main.tf`. Add the arguments and nested blocks required for aws_security_group. Use the visible constraints as your checklist before you run the tests.

**When to use it:** Use EC2 when you need a virtual machine you control directly, or as a building block inside an autoscaling or container platform.

**How to approach it:** Open `main.tf` and work inside the single TODO region. Change one requirement at a time: add the named block, argument or reference, then run the tests. When a check fails, match its wording to the constraints and fix only the block it names.


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
