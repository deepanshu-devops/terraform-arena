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

**What to do:** Complete the marked TODO in `main.tf`. Add the subnet list and the tag map. Use the visible constraints as your checklist before you run the tests.

**When to use it:** Reach for this whenever you add a new block or argument by hand rather than copying generated code.

**How to approach it:** Open `main.tf` and work inside the single TODO region. Change one requirement at a time: add the named block, argument or reference, then run the tests. When a check fails, match its wording to the constraints and fix only the block it names.


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
