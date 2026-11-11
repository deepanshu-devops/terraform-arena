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
