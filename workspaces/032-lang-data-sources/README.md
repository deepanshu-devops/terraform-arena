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

**What to do:** Complete the marked region in `main.tf`. The work is inside `data "aws_ami" "latest"`. Add most_recent, owners and a filter so the newest Amazon Linux image is discovered. Use the visible constraints as the checklist for names, values and references before you run the tests.

**When to use it:** Use EC2 when you need a virtual machine you control directly, or as a building block inside an autoscaling or container platform.

**How to approach it:** Open `main.tf` and work only inside `data "aws_ami" "latest"`. Use this code shape: most_recent; owners; filter { name; values }. Keep the block header and braces, indent nested blocks by two spaces, and add one argument or nested block at a time. Run the tests after each small change so the first failure points at the next name to fix.


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
