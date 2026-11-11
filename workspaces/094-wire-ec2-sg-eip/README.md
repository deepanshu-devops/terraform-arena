# 094 - EC2 Instance + Security Group + EIP

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
python judge.py test 94 --dir workspaces/094-wire-ec2-sg-eip
```

> Hidden test details are only revealed after a submission.
