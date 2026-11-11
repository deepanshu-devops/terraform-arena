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

**What to do:** Complete the marked region in `main.tf`. The work is inside `resource "aws_iam_policy" "this"`. Add the arguments and nested blocks required for aws_iam_policy. Use the visible constraints as the checklist for names, values and references before you run the tests.

**When to use it:** Create IAM resources when a workload or operator needs narrowly scoped permissions, and prefer roles and temporary credentials over long-lived keys.

**How to approach it:** Open `main.tf` and work only inside `resource "aws_iam_policy" "this"`. Use this code shape: name; policy. Use the already-declared references instead of hardcoded values: `data.aws_iam_policy_document.this`. Keep the block header and braces, indent nested blocks by two spaces, and add one argument or nested block at a time. Run the tests after each small change so the first failure points at the next name to fix.


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
