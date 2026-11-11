# 083 - Encrypted EBS Volume

**Level:** Level 3 - Real Infrastructure  
**Difficulty:** Easy  
**Points:** 60  
**Tags:** aws, ec2, security, storage

## Scenario

Create a small encrypted EBS volume for a single instance, keeping size within the free tier.

## What to complete

- File: `main.tf`
- Task: Complete the aws_ebs_volume resource
- Add the arguments and nested blocks required for aws_ebs_volume.

## Hints

**Why it matters:** EC2 teaches the core lifecycle of compute: image, instance type, networking, storage and safe replacement.

**What to do:** Complete the marked region in `main.tf`. The work is inside `resource "aws_ebs_volume" "this"`. Add the arguments and nested blocks required for aws_ebs_volume. Use the visible constraints as the checklist for names, values and references before you run the tests.

**When to use it:** Use EC2 when you need a virtual machine you control directly, or as a building block inside an autoscaling or container platform.

**How to approach it:** Open `main.tf` and work only inside `resource "aws_ebs_volume" "this"`. Use this code shape: availability_zone; size; encrypted. Use the already-declared references instead of hardcoded values: `var.availability_zone`. Keep the block header and braces, indent nested blocks by two spaces, and add one argument or nested block at a time. Run the tests after each small change so the first failure points at the next name to fix.


## Constraints

- encrypted = true.
- size <= 20 GB.
- Availability zone from var.availability_zone.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `availability_zone` | `string` | `us-east-1a` |

## Expected resources

- `aws_ebs_volume`

## Expected outputs

- `volume_id`

## How to test

```powershell
python judge.py test 83 --dir workspaces/083-harden-ebs-encryption
```

> Hidden test details are only revealed after a submission.
