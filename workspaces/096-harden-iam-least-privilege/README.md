# 096 - Least-Privilege IAM Policy

**Level:** Level 4 - Composition  
**Difficulty:** Hard  
**Points:** 120  
**Tags:** aws, iam, security

## Scenario

A Lambda role must read and write only one DynamoDB table. Replace the wildcard policy with a scoped one.

## What to complete

- File: `main.tf`
- Task: Complete the aws_iam_policy resource
- Add the arguments and nested blocks required for aws_iam_policy.

## Constraints

- Use a data.aws_iam_policy_document.
- Grant only required dynamodb actions.
- Scope resources to the table ARN.
- No wildcard actions.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `policy_name` | `string` | `app-policy` |
| `table_name` | `string` | `items` |

## Expected resources

- `aws_iam_policy`
- `aws_dynamodb_table`

## Expected outputs

- `policy_arn`

## How to test

```powershell
python judge.py test 96 --dir workspaces/096-harden-iam-least-privilege
```

> Hidden test details are only revealed after a submission.
