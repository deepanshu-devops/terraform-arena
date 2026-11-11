# 088 - Enforce IMDSv2 on EC2

**Level:** Level 3 - Real Infrastructure  
**Difficulty:** Medium  
**Points:** 90  
**Tags:** aws, ec2, security

## Scenario

The security team requires IMDSv2 on every instance launched by the template. Enforce tokens and limit hop count.

## What to complete

- File: `main.tf`
- Task: Complete the aws_launch_template resource
- Add the arguments and nested blocks required for aws_launch_template.

## Constraints

- Use aws_launch_template.
- metadata_options.http_tokens = required.
- metadata_options.http_endpoint = enabled.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `ami_id` | `string` | `required` |
| `instance_type` | `string` | `t2.micro` |

## Expected resources

- `aws_launch_template`

## Expected outputs

- `launch_template_id`

## How to test

```powershell
python judge.py test 88 --dir workspaces/088-harden-ec2-imdsv2
```

> Hidden test details are only revealed after a submission.
