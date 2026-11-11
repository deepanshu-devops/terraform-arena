# 098 - Enforce IMDSv2 on EC2

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

## Hints

**Why it matters:** EC2 teaches the core lifecycle of compute: image, instance type, networking, storage and safe replacement.

**What to do:** Complete the marked region in `main.tf`. The work is inside `resource "aws_launch_template" "this"`. Add the arguments and nested blocks required for aws_launch_template. Use the visible constraints as the checklist for names, values and references before you run the tests.

**When to use it:** Use EC2 when you need a virtual machine you control directly, or as a building block inside an autoscaling or container platform.

**How to approach it:** Open `main.tf` and work only inside `resource "aws_launch_template" "this"`. Use this code shape: name; image_id; instance_type; metadata_options { http_tokens; http_endpoint }. Use the already-declared references instead of hardcoded values: `var.ami_id`, `var.instance_type`. Keep the block header and braces, indent nested blocks by two spaces, and add one argument or nested block at a time. Run the tests after each small change so the first failure points at the next name to fix.


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
python judge.py test 98 --dir workspaces/098-harden-ec2-imdsv2
```

> Hidden test details are only revealed after a submission.
