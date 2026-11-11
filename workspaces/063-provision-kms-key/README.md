# 063 - Provision KMS Customer Key

**Level:** Level 2 - First Resources  
**Difficulty:** Easy  
**Points:** 50  
**Tags:** aws, kms, provisioning

## Scenario

Your platform team needs KMS Customer Key for a rotating customer-managed encryption key. Write a reusable Terraform configuration that provisions it, drives every input through variables, applies the standard tags, and exports the operational identifiers.

## What to complete

- File: `main.tf`
- Task: Complete the aws_kms_key resource
- Add the arguments and nested blocks required for aws_kms_key.

## Hints

**Why it matters:** Encryption keys are a security boundary. Key policies and rotation settings determine who can protect and recover data.

**What to do:** Complete the marked region in `main.tf`. The work is inside `resource "aws_kms_key" "this"`. Add the arguments and nested blocks required for aws_kms_key. Use the visible constraints as the checklist for names, values and references before you run the tests.

**When to use it:** Use a customer-managed key when you need control over encryption policy, rotation or cross-account access.

**How to approach it:** Open `main.tf` and work only inside `resource "aws_kms_key" "this"`. Use this code shape: description; tags; enable_key_rotation; deletion_window_in_days. Use the already-declared references instead of hardcoded values: `var.project_name`, `var.environment`. Keep the block header and braces, indent nested blocks by two spaces, and add one argument or nested block at a time. Run the tests after each small change so the first failure points at the next name to fix.


## Constraints

- Provider: aws (region from var.aws_region).
- Create exactly one resource of type aws_kms_key.
- All configurable values must come from variables declared in variables.tf.
- No hardcoded AWS credentials.
- Code must pass terraform fmt conventions (2-space indents, trailing newline, no tabs).
- Tag the resource with Project, Environment and ManagedBy = "terraform".
- Expose outputs: key_arn, key_id.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `environment` | `string` | `dev` |
| `project_name` | `string` | `terraform-practice` |
| `aws_region` | `string` | `us-east-1` |

## Expected resources

- `aws_kms_key`

## Expected outputs

- `key_arn`
- `key_id`

## How to test

```powershell
python judge.py test 63 --dir workspaces/063-provision-kms-key
```

> Hidden test details are only revealed after a submission.
