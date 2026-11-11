# 029 - Explicit depends_on

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

## Hints

**Why it matters:** `aws_instance` is a real building block in production configurations. The exercise isolates one decision so you can recognise the same shape when it appears inside a larger module.

**What to do:** Complete the marked TODO in `main.tf`. Make the instance wait for the security group with depends_on. Use the visible constraints as your checklist before you run the tests.

**When to use it:** Use this pattern when the requirement is part of a reusable configuration that another person or environment must be able to reproduce.

**How to approach it:** Open `main.tf` and work inside the single TODO region. Change one requirement at a time: add the named block, argument or reference, then run the tests. When a check fails, match its wording to the constraints and fix only the block it names.


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
python judge.py test 29 --dir workspaces/029-lang-depends-on
```

> Hidden test details are only revealed after a submission.
