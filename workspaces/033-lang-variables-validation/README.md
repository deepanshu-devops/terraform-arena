# 033 - Variable Validation

**Level:** Level 1 - Terraform Language  
**Difficulty:** Easy  
**Points:** 60  
**Tags:** terraform, variables, validation

## Scenario

Declare bucket_name with a validation block that enforces lowercase letters, digits and hyphens, and a 3-63 length.

## What to complete

- File: `variables.tf`
- Task: Complete the validation block for bucket_name
- Add a condition and error_message that enforce the documented bucket naming rules.

## Hints

**Why it matters:** Input variables separate configuration from implementation. They let one module serve dev, staging and production without editing the resource code, and they give reviewers one obvious place to inspect change.

**What to do:** Complete the marked TODO in `variables.tf`. Add a condition and error_message that enforce the documented bucket naming rules. Use the visible constraints as your checklist before you run the tests.

**When to use it:** Use a variable when a value differs by environment, comes from a caller, or must be supplied securely at apply time. Keep truly stable constants in locals instead.

**How to approach it:** Open `variables.tf` and work inside the single TODO region. Change one requirement at a time: add the named block, argument or reference, then run the tests. When a check fails, match its wording to the constraints and fix only the block it names.


## Constraints

- Use can(regex(...)) or a regex() rule.
- Enforce length 3-63.
- Use the variable for the bucket name.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `bucket_name` | `string` | `required` |

## Expected resources

- `aws_s3_bucket`

## Expected outputs

- `bucket_id`

## How to test

```powershell
python judge.py test 33 --dir workspaces/033-lang-variables-validation
```

> Hidden test details are only revealed after a submission.
