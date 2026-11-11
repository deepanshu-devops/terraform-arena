# 060 - Provision IAM Policy

**Level:** Level 2 - First Resources  
**Difficulty:** Easy  
**Points:** 50  
**Tags:** aws, iam, provisioning

## Scenario

Your platform team needs IAM Policy for a scoped permission set. Write a reusable Terraform configuration that provisions it, drives every input through variables, applies the standard tags, and exports the operational identifiers.

## What to complete

- File: `main.tf`
- Task: Complete the aws_iam_policy resource
- Add the arguments and nested blocks required for aws_iam_policy.

## Hints

**Why it matters:** IAM is the main authorization boundary in AWS. Least-privilege policies prevent one compromised workload from becoming an account-wide incident.

**What to do:** Complete the marked region in `main.tf`. The work is inside `resource "aws_iam_policy" "this"`. Add the arguments and nested blocks required for aws_iam_policy. Use the visible constraints as the checklist for names, values and references before you run the tests.

**When to use it:** Create IAM resources when a workload or operator needs narrowly scoped permissions, and prefer roles and temporary credentials over long-lived keys.

**How to approach it:** Open `main.tf` and work only inside `resource "aws_iam_policy" "this"`. Use this code shape: name; tags; policy. Use the already-declared references instead of hardcoded values: `var.policy_name`, `var.project_name`, `var.environment`, `aws_dynamodb_table.this.arn`. Keep the block header and braces, indent nested blocks by two spaces, and add one argument or nested block at a time. Run the tests after each small change so the first failure points at the next name to fix.


## Constraints

- Provider: aws (region from var.aws_region).
- Create exactly one resource of type aws_iam_policy.
- All configurable values must come from variables declared in variables.tf.
- No hardcoded AWS credentials.
- Code must pass terraform fmt conventions (2-space indents, trailing newline, no tabs).
- Tag the resource with Project, Environment and ManagedBy = "terraform".
- Expose outputs: policy_arn.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `policy_name` | `string` | `app-policy` |
| `environment` | `string` | `dev` |
| `project_name` | `string` | `terraform-practice` |
| `aws_region` | `string` | `us-east-1` |

## Expected resources

- `aws_iam_policy`

## Expected outputs

- `policy_arn`

## How to test

```powershell
python judge.py test 60 --dir workspaces/060-provision-iam-policy
```

> Hidden test details are only revealed after a submission.
