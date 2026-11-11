# 112 - EC2 Instance + Security Group + EIP

**Level:** Level 4 - Composition  
**Difficulty:** Medium  
**Points:** 120  
**Tags:** aws, ec2, networking

## Scenario

Launch an instance in a subnet, attach a security group, and associate an Elastic IP.

## What to complete

- File: `main.tf`
- Task: Complete the aws_instance resource
- Add the arguments and nested blocks required for aws_instance.

## Hints

**Why it matters:** EC2 teaches the core lifecycle of compute: image, instance type, networking, storage and safe replacement.

**What to do:** Complete the marked region in `main.tf`. The work is inside `resource "aws_instance" "this"`. Add the arguments and nested blocks required for aws_instance. Use the visible constraints as the checklist for names, values and references before you run the tests.

**When to use it:** Use EC2 when you need a virtual machine you control directly, or as a building block inside an autoscaling or container platform.

**How to approach it:** Open `main.tf` and work only inside `resource "aws_instance" "this"`. Use this code shape: ami; instance_type; subnet_id; vpc_security_group_ids; metadata_options { http_tokens }. Use the already-declared references instead of hardcoded values: `var.subnet_id`, `aws_security_group.this.id`. Keep the block header and braces, indent nested blocks by two spaces, and add one argument or nested block at a time. Run the tests after each small change so the first failure points at the next name to fix.


## Constraints

- Instance uses the SG and subnet.
- EIP associates with the instance.
- Instance has IMDSv2.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `ami_id` | `string` | `required` |
| `instance_type` | `string` | `t2.micro` |
| `subnet_id` | `string` | `required` |
| `vpc_id` | `string` | `required` |
| `project_name` | `string` | `terraform-practice` |
| `environment` | `string` | `dev` |
| `aws_region` | `string` | `us-east-1` |

## Expected resources

- `aws_security_group`
- `aws_instance`
- `aws_eip`

## Expected outputs

- `instance_id`
- `public_ip`

## How to test

```powershell
python judge.py test 112 --dir workspaces/112-wire-ec2-sg-eip
```

> Hidden test details are only revealed after a submission.
