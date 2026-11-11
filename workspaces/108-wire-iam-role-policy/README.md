# 108 - IAM Role + Policy + Attachment

**Level:** Level 4 - Composition  
**Difficulty:** Medium  
**Points:** 100  
**Tags:** aws, iam, security

## Scenario

Create a Lambda execution role, a scoped policy, and attach the policy to the role.

## What to complete

- File: `main.tf`
- Task: Complete the aws_iam_role_policy_attachment resource
- Add the arguments and nested blocks required for aws_iam_role_policy_attachment.

## Hints

**Why it matters:** IAM is the main authorization boundary in AWS. Least-privilege policies prevent one compromised workload from becoming an account-wide incident.

**What to do:** Complete the marked TODO in `main.tf`. Add the arguments and nested blocks required for aws_iam_role_policy_attachment. Use the visible constraints as your checklist before you run the tests.

**When to use it:** Create IAM resources when a workload or operator needs narrowly scoped permissions, and prefer roles and temporary credentials over long-lived keys.

**How to approach it:** Open `main.tf` and work inside the single TODO region. Change one requirement at a time: add the named block, argument or reference, then run the tests. When a check fails, match its wording to the constraints and fix only the block it names.


## Constraints

- Role trusts lambda.amazonaws.com.
- Policy has no wildcard actions.
- Attachment links policy and role.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `role_name` | `string` | `app-role` |
| `policy_name` | `string` | `app-policy` |
| `project_name` | `string` | `terraform-practice` |
| `environment` | `string` | `dev` |
| `aws_region` | `string` | `us-east-1` |

## Expected resources

- `aws_iam_role`
- `aws_iam_policy`
- `aws_iam_role_policy_attachment`

## Expected outputs

- `role_arn`
- `policy_arn`

## How to test

```powershell
python judge.py test 108 --dir workspaces/108-wire-iam-role-policy
```

> Hidden test details are only revealed after a submission.
