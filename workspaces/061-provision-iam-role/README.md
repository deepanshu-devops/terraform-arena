# 061 - Provision IAM Role

**Level:** Level 2 - First Resources  
**Difficulty:** Easy  
**Points:** 50  
**Tags:** aws, iam, provisioning

## Scenario

Your platform team needs IAM Role for a service role with a trust policy. Write a reusable Terraform configuration that provisions it, drives every input through variables, applies the standard tags, and exports the operational identifiers.

## What to complete

- File: `main.tf`
- Task: Complete the aws_iam_role resource
- Add the arguments and nested blocks required for aws_iam_role.

## Hints

**Why it matters:** IAM is the main authorization boundary in AWS. Least-privilege policies prevent one compromised workload from becoming an account-wide incident.

**What to do:** Complete the marked region in `main.tf`. The work is inside `resource "aws_iam_role" "this"`. Add the arguments and nested blocks required for aws_iam_role. Use the visible constraints as the checklist for names, values and references before you run the tests.

**When to use it:** Create IAM resources when a workload or operator needs narrowly scoped permissions, and prefer roles and temporary credentials over long-lived keys.

**How to approach it:** Open `main.tf` and work only inside `resource "aws_iam_role" "this"`. Use this code shape: name; tags; assume_role_policy. Use the already-declared references instead of hardcoded values: `var.role_name`, `var.project_name`, `var.environment`. Keep the block header and braces, indent nested blocks by two spaces, and add one argument or nested block at a time. Run the tests after each small change so the first failure points at the next name to fix.


## Constraints

- Provider: aws (region from var.aws_region).
- Create exactly one resource of type aws_iam_role.
- All configurable values must come from variables declared in variables.tf.
- No hardcoded AWS credentials.
- Code must pass terraform fmt conventions (2-space indents, trailing newline, no tabs).
- Tag the resource with Project, Environment and ManagedBy = "terraform".
- Expose outputs: role_arn.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `role_name` | `string` | `app-role` |
| `trusted_service` | `string` | `lambda.amazonaws.com` |
| `environment` | `string` | `dev` |
| `project_name` | `string` | `terraform-practice` |
| `aws_region` | `string` | `us-east-1` |

## Expected resources

- `aws_iam_role`

## Expected outputs

- `role_arn`

## How to test

```powershell
python judge.py test 61 --dir workspaces/061-provision-iam-role
```

> Hidden test details are only revealed after a submission.
