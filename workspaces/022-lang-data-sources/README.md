# 022 - Discover an AMI With a Data Source

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
python judge.py test 22 --dir workspaces/022-lang-data-sources
```

> Hidden test details are only revealed after a submission.
