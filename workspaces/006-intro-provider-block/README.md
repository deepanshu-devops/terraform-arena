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

**What to do:** Complete the marked TODO in `main.tf`. Set the provider region from the declared variable. Use the visible constraints as your checklist before you run the tests.

**When to use it:** Configure a provider once per module and pass credentials through the environment or a secure mechanism, never through committed literals.

**How to approach it:** Open `main.tf` and work inside the single TODO region. Change one requirement at a time: add the named block, argument or reference, then run the tests. When a check fails, match its wording to the constraints and fix only the block it names.


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
