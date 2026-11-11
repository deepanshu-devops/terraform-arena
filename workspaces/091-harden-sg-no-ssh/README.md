# 091 - Security Group Without Public SSH

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
python judge.py test 91 --dir workspaces/091-harden-sg-no-ssh
```

> Hidden test details are only revealed after a submission.
