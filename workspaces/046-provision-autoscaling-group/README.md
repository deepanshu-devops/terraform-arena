# 046 - Provision Auto Scaling Group

**Level:** Level 2 - First Resources  
**Difficulty:** Easy  
**Points:** 50  
**Tags:** aws, ec2, provisioning

## Scenario

Your platform team needs Auto Scaling Group for elastic capacity across subnets. Write a reusable Terraform configuration that provisions it, drives every input through variables, applies the standard tags, and exports the operational identifiers.

## What to complete

- File: `main.tf`
- Task: Complete the aws_autoscaling_group resource
- Add the arguments and nested blocks required for aws_autoscaling_group.

## Hints

**Why it matters:** EC2 teaches the core lifecycle of compute: image, instance type, networking, storage and safe replacement.

**What to do:** Complete the marked region in `main.tf`. The work is inside `resource "aws_autoscaling_group" "this"`. Add the arguments and nested blocks required for aws_autoscaling_group. Use the visible constraints as the checklist for names, values and references before you run the tests.

**When to use it:** Use EC2 when you need a virtual machine you control directly, or as a building block inside an autoscaling or container platform.

**How to approach it:** Open `main.tf` and work only inside `resource "aws_autoscaling_group" "this"`. Use this code shape: name; min_size; max_size; desired_capacity; vpc_zone_identifier; launch_template { id; version }. Use the already-declared references instead of hardcoded values: `var.asg_min`, `var.asg_max`, `var.asg_desired`, `var.subnet_ids`, `aws_launch_template.this.id`. Keep the block header and braces, indent nested blocks by two spaces, and add one argument or nested block at a time. Run the tests after each small change so the first failure points at the next name to fix.


## Constraints

- Provider: aws (region from var.aws_region).
- Create exactly one resource of type aws_autoscaling_group.
- All configurable values must come from variables declared in variables.tf.
- No hardcoded AWS credentials.
- Code must pass terraform fmt conventions (2-space indents, trailing newline, no tabs).
- Expose outputs: asg_name.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `asg_min` | `number` | `1` |
| `asg_max` | `number` | `2` |
| `asg_desired` | `number` | `1` |
| `subnet_ids` | `list(string)` | `required` |
| `aws_region` | `string` | `us-east-1` |

## Expected resources

- `aws_autoscaling_group`

## Expected outputs

- `asg_name`

## How to test

```powershell
python judge.py test 46 --dir workspaces/046-provision-autoscaling-group
```

> Hidden test details are only revealed after a submission.
