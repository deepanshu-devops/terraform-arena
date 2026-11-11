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

**What to do:** Complete the marked TODO in `main.tf`. Add the arguments and nested blocks required for aws_iam_policy. Use the visible constraints as your checklist before you run the tests.

**When to use it:** Create IAM resources when a workload or operator needs narrowly scoped permissions, and prefer roles and temporary credentials over long-lived keys.

**How to approach it:** Open `main.tf` and work inside the single TODO region. Change one requirement at a time: add the named block, argument or reference, then run the tests. When a check fails, match its wording to the constraints and fix only the block it names.


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
