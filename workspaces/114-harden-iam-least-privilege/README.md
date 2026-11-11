# 114 - Least-Privilege IAM Policy

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

## Hints

**Why it matters:** IAM is the main authorization boundary in AWS. Least-privilege policies prevent one compromised workload from becoming an account-wide incident.

**What to do:** Complete the marked TODO in `main.tf`. Add the arguments and nested blocks required for aws_iam_policy. Use the visible constraints as your checklist before you run the tests.

**When to use it:** Create IAM resources when a workload or operator needs narrowly scoped permissions, and prefer roles and temporary credentials over long-lived keys.

**How to approach it:** Open `main.tf` and work inside the single TODO region. Change one requirement at a time: add the named block, argument or reference, then run the tests. When a check fails, match its wording to the constraints and fix only the block it names.


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
python judge.py test 114 --dir workspaces/114-harden-iam-least-privilege
```

> Hidden test details are only revealed after a submission.
