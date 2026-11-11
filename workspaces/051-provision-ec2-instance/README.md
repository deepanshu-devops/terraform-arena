# 051 - Provision EC2 Instance

**Level:** Level 2 - First Resources  
**Difficulty:** Easy  
**Points:** 50  
**Tags:** aws, ec2, provisioning

## Scenario

Your platform team needs EC2 Instance for a virtual machine for a stateless service. Write a reusable Terraform configuration that provisions it, drives every input through variables, applies the standard tags, and exports the operational identifiers.

## What to complete

- File: `main.tf`
- Task: Complete the aws_instance resource
- Add the arguments and nested blocks required for aws_instance.

## Hints

**Why it matters:** EC2 teaches the core lifecycle of compute: image, instance type, networking, storage and safe replacement.

**What to do:** Complete the marked region in `main.tf`. The work is inside `resource "aws_instance" "this"`. Add the arguments and nested blocks required for aws_instance. Use the visible constraints as the checklist for names, values and references before you run the tests.

**When to use it:** Use EC2 when you need a virtual machine you control directly, or as a building block inside an autoscaling or container platform.

**How to approach it:** Open `main.tf` and work only inside `resource "aws_instance" "this"`. Use this code shape: ami; instance_type; tags; subnet_id; associate_public_ip_address; metadata_options { http_tokens }. Use the already-declared references instead of hardcoded values: `var.ami_id`, `var.instance_type`, `var.project_name`, `var.environment`, `var.subnet_id`. Keep the block header and braces, indent nested blocks by two spaces, and add one argument or nested block at a time. Run the tests after each small change so the first failure points at the next name to fix.


## Constraints

- Provider: aws (region from var.aws_region).
- Create exactly one resource of type aws_instance.
- All configurable values must come from variables declared in variables.tf.
- No hardcoded AWS credentials.
- Code must pass terraform fmt conventions (2-space indents, trailing newline, no tabs).
- Tag the resource with Project, Environment and ManagedBy = "terraform".
- Expose outputs: instance_id.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `ami_id` | `string` | `required` |
| `instance_type` | `string` | `t2.micro` |
| `subnet_id` | `string` | `required` |
| `environment` | `string` | `dev` |
| `project_name` | `string` | `terraform-practice` |
| `aws_region` | `string` | `us-east-1` |

## Expected resources

- `aws_instance`

## Expected outputs

- `instance_id`

## How to test

```powershell
python judge.py test 51 --dir workspaces/051-provision-ec2-instance
```

> Hidden test details are only revealed after a submission.
