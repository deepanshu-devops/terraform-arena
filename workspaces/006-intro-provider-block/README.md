# 006 - Provider and Version Blocks

**Level:** Level 0 - HCL Foundations  
**Difficulty:** Easy  
**Points:** 50  
**Tags:** terraform, providers, versions

## Scenario

The terraform block declares required providers and versions. The provider block configures AWS. Complete the provider block so the region comes from a variable.

## What to complete

- File: `main.tf`
- Task: Complete the provider block
- Set the provider region from the declared variable.

## Hints

**Why it matters:** Providers tell Terraform which API to call and how to authenticate. Pinning the provider and keeping settings in variables makes a configuration portable and reproducible.

**What to do:** Complete the marked region in `main.tf`. The work is inside `provider "aws"`. Set the provider region from the declared variable. Use the visible constraints as the checklist for names, values and references before you run the tests.

**When to use it:** Configure a provider once per module and pass credentials through the environment or a secure mechanism, never through committed literals.

**How to approach it:** Open `main.tf` and work only inside `provider "aws"`. Use this code shape: region. Use the already-declared references instead of hardcoded values: `var.aws_region`. Keep the block header and braces, indent nested blocks by two spaces, and add one argument or nested block at a time. Run the tests after each small change so the first failure points at the next name to fix.


## Constraints

- Require hashicorp/aws in versions.tf.
- Configure provider aws with region = var.aws_region.
- Declare aws_region with a default of us-east-1.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `aws_region` | `string` | `us-east-1` |

## Expected resources

- (see constraints)

## Expected outputs

- (none)

## How to test

```powershell
python judge.py test 6 --dir workspaces/006-intro-provider-block
```

> Hidden test details are only revealed after a submission.
