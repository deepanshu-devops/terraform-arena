# 005 - Lists and Maps

**Level:** Level 0 - HCL Foundations  
**Difficulty:** Easy  
**Points:** 50  
**Tags:** terraform, hcl, collections

## Scenario

Lists and maps are first-class HCL values. Define a list of subnet CIDRs and a map of tags in a locals block.

## What to complete

- File: `main.tf`
- Task: Complete the collections
- Add the subnet list and the tag map.

## Hints

**Why it matters:** HCL is the language Terraform evaluates. Small syntax mistakes here turn into confusing plan errors later, so slow, deliberate practice pays off.

**What to do:** Complete the marked region in `main.tf`. The work is inside `locals`. Add the subnet list and the tag map. Use the visible constraints as the checklist for names, values and references before you run the tests.

**When to use it:** Reach for this whenever you add a new block or argument by hand rather than copying generated code.

**How to approach it:** Open `main.tf` and work only inside `locals`. Use this code shape: subnets; tags. Keep the block header and braces, indent nested blocks by two spaces, and add one argument or nested block at a time. Run the tests after each small change so the first failure points at the next name to fix.


## Constraints

- Define a subnets list with two CIDR strings.
- Define a tags map with Project and Environment keys.

## Input variables

| Name | Type | Default |
| --- | --- | --- |

## Expected resources

- (see constraints)

## Expected outputs

- (none)

## How to test

```powershell
python judge.py test 5 --dir workspaces/005-intro-hcl-collections
```

> Hidden test details are only revealed after a submission.
