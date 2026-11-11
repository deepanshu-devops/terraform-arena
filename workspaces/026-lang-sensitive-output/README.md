# 026 - Sensitive Output

**Level:** Level 1 - Terraform Language  
**Difficulty:** Easy  
**Points:** 50  
**Tags:** terraform, outputs, security

## Scenario

Expose a connection string but mark the output as sensitive so it is redacted in plan output.

## What to complete

- File: `outputs.tf`
- Task: Mark the output as sensitive
- Add the sensitive argument to the bucket_arn output.

## Hints

**Why it matters:** Outputs are the public surface of a configuration or module. They let callers and operators consume values without reaching into internal resource addresses.

**What to do:** Complete the marked region in `outputs.tf`. The work is inside `output "bucket_arn"`. Add the sensitive argument to the bucket_arn output. Use the visible constraints as the checklist for names, values and references before you run the tests.

**When to use it:** Export an identifier, endpoint or name when another configuration, a module consumer, or an operator needs it. Mark secrets sensitive.

**How to approach it:** Open `outputs.tf` and work only inside `output "bucket_arn"`. Use this code shape: sensitive. Keep the block header and braces, indent nested blocks by two spaces, and add one argument or nested block at a time. Run the tests after each small change so the first failure points at the next name to fix.


## Constraints

- Create an output.
- Set sensitive = true.
- Provision an S3 bucket or similar resource.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `bucket_name` | `string` | `required` |

## Expected resources

- `aws_s3_bucket`

## Expected outputs

- `bucket_arn`

## How to test

```powershell
python judge.py test 26 --dir workspaces/026-lang-sensitive-output
```

> Hidden test details are only revealed after a submission.
