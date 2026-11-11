# 073 - Encrypted EBS Volume

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
python judge.py test 73 --dir workspaces/073-harden-ebs-encryption
```

> Hidden test details are only revealed after a submission.
