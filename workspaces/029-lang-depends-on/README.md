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

**What to do:** Complete the marked region in `main.tf`. The work is inside `resource "aws_instance" "this"`. Make the instance wait for the security group with depends_on. Use the visible constraints as the checklist for names, values and references before you run the tests.

**When to use it:** Use this pattern when the requirement is part of a reusable configuration that another person or environment must be able to reproduce.

**How to approach it:** Open `main.tf` and work only inside `resource "aws_instance" "this"`. Use this code shape: depends_on. Use the already-declared references instead of hardcoded values: `aws_security_group.this`. Keep the block header and braces, indent nested blocks by two spaces, and add one argument or nested block at a time. Run the tests after each small change so the first failure points at the next name to fix.


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
