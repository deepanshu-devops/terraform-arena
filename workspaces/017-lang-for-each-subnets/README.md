# 017 - Create Subnets With for_each

**Level:** Level 1 - Terraform Language  
**Difficulty:** Medium  
**Points:** 95  
**Tags:** terraform, for_each, networking

## Scenario

Create subnets from a map with for_each so adding a subnet is just a map entry.

## What to complete

- File: `main.tf`
- Task: Complete the aws_subnet block
- Use for_each over the subnet map and reference each.key/value.

## Constraints

- Use for_each over a map variable.
- Reference each.key/each.value.
- One resource block.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `vpc_id` | `string` | `required` |
| `subnets` | `map(string)` | `{'public-a': '10.0.1.0/24', 'public-b': '10.0.2.0/24'}` |

## Expected resources

- `aws_subnet`

## Expected outputs

- `subnet_ids`

## How to test

```powershell
python judge.py test 17 --dir workspaces/017-lang-for-each-subnets
```

> Hidden test details are only revealed after a submission.
