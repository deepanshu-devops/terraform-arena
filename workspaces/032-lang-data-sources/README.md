# 032 - Discover an AMI With a Data Source

**Level:** Level 1 - Terraform Language  
**Difficulty:** Easy  
**Points:** 60  
**Tags:** terraform, data-sources, ec2

## Scenario

Discover the latest Amazon Linux AMI with a data source and use it to launch an instance.

## What to complete

- File: `main.tf`
- Task: Complete the aws_ami data source
- Add most_recent, owners and a filter so the newest Amazon Linux image is discovered.

## Hints

**Why it matters:** EC2 teaches the core lifecycle of compute: image, instance type, networking, storage and safe replacement.

**What to do:** Complete the marked TODO in `main.tf`. Add most_recent, owners and a filter so the newest Amazon Linux image is discovered. Use the visible constraints as your checklist before you run the tests.

**When to use it:** Use EC2 when you need a virtual machine you control directly, or as a building block inside an autoscaling or container platform.

**How to approach it:** Open `main.tf` and work inside the single TODO region. Change one requirement at a time: add the named block, argument or reference, then run the tests. When a check fails, match its wording to the constraints and fix only the block it names.


## Constraints

- Use data.aws_ami.
- image_id references the data source.
- Instance type from a variable.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `instance_type` | `string` | `t2.micro` |
| `subnet_id` | `string` | `required` |

## Expected resources

- `aws_instance`

## Expected outputs

- `instance_id`

## How to test

```powershell
python judge.py test 32 --dir workspaces/032-lang-data-sources
```

> Hidden test details are only revealed after a submission.
