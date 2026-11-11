# 090 - IAM Role + Policy + Attachment

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
python judge.py test 90 --dir workspaces/090-wire-iam-role-policy
```

> Hidden test details are only revealed after a submission.
