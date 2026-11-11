# 050 - Provision EBS Volume

**Level:** Level 2 - First Resources  
**Difficulty:** Easy  
**Points:** 50  
**Tags:** aws, ec2, provisioning

## Scenario

Your platform team needs EBS Volume for block storage for a single EC2 instance. Write a reusable Terraform configuration that provisions it, drives every input through variables, applies the standard tags, and exports the operational identifiers.

## What to complete

- File: `main.tf`
- Task: Complete the aws_ebs_volume resource
- Add the arguments and nested blocks required for aws_ebs_volume.

## Hints

**Why it matters:** EC2 teaches the core lifecycle of compute: image, instance type, networking, storage and safe replacement.

**What to do:** Complete the marked TODO in `main.tf`. Add the arguments and nested blocks required for aws_ebs_volume. Use the visible constraints as your checklist before you run the tests.

**When to use it:** Use EC2 when you need a virtual machine you control directly, or as a building block inside an autoscaling or container platform.

**How to approach it:** Open `main.tf` and work inside the single TODO region. Change one requirement at a time: add the named block, argument or reference, then run the tests. When a check fails, match its wording to the constraints and fix only the block it names.


## Constraints

- Provider: aws (region from var.aws_region).
- Create exactly one resource of type aws_ebs_volume.
- All configurable values must come from variables declared in variables.tf.
- No hardcoded AWS credentials.
- Code must pass terraform fmt conventions (2-space indents, trailing newline, no tabs).
- Tag the resource with Project, Environment and ManagedBy = "terraform".
- Expose outputs: volume_id.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `availability_zone` | `string` | `us-east-1a` |
| `environment` | `string` | `dev` |
| `project_name` | `string` | `terraform-practice` |
| `aws_region` | `string` | `us-east-1` |

## Expected resources

- `aws_ebs_volume`

## Expected outputs

- `volume_id`

## How to test

```powershell
python judge.py test 50 --dir workspaces/050-provision-ebs-volume
```

> Hidden test details are only revealed after a submission.
