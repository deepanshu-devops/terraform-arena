# 035 - Create Subnets With for_each

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

## Hints

**Why it matters:** for_each creates one instance per stable key. Adding or removing an entry changes only that instance, whereas an index-based list can shift every later instance when the order changes.

**What to do:** Complete the marked region in `main.tf`. The work is inside `resource "aws_subnet" "this"`. Use for_each over the subnet map and reference each.key/value. Use the visible constraints as the checklist for names, values and references before you run the tests.

**When to use it:** Use for_each when each instance has a durable identity, usually from a map or a set of strings. Use count for identical instances where position is the identity.

**How to approach it:** Open `main.tf` and work only inside `resource "aws_subnet" "this"`. Use this code shape: cidr_block; vpc_id; for_each; availability_zone. Use the already-declared references instead of hardcoded values: `each.value`, `var.vpc_id`, `var.subnets`, `each.key`. Keep the block header and braces, indent nested blocks by two spaces, and add one argument or nested block at a time. Run the tests after each small change so the first failure points at the next name to fix.


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
python judge.py test 35 --dir workspaces/035-lang-for-each-subnets
```

> Hidden test details are only revealed after a submission.
