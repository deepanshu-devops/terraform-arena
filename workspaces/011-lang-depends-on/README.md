# 011 - Explicit depends_on

**Level:** Level 1 - Terraform Language  
**Difficulty:** Easy  
**Points:** 55  
**Tags:** terraform, depends_on, ordering

## Scenario

Force the instance to wait for the security group using an explicit depends_on.

## What to complete

- File: `main.tf`
- Task: Add the explicit dependency
- Make the instance wait for the security group with depends_on.

## Constraints

- Create a security group and an instance.
- Instance has depends_on = [aws_security_group...].
- Instance uses the SG.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `ami_id` | `string` | `required` |
| `instance_type` | `string` | `t2.micro` |
| `subnet_id` | `string` | `required` |
| `vpc_id` | `string` | `required` |

## Expected resources

- `aws_instance`
- `aws_security_group`

## Expected outputs

- `instance_id`

## How to test

```powershell
python judge.py test 11 --dir workspaces/011-lang-depends-on
```

> Hidden test details are only revealed after a submission.
