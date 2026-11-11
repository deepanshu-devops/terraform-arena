# 018 - Tutorial: Look Up Values in a Map

**Level:** Level 0 - HCL Foundations  
**Difficulty:** Easy  
**Points:** 66  
**Tags:** terraform, tutorial, collections

## Scenario

A map gives every value a name. Instead of remembering an index, a caller looks up a key. Build a map of instance sizes and read one entry by key.

## What to complete

- File: `main.tf`
- Task: Create the lookup map
- Add a two-entry map with a small dev size and a larger prod size.

## Hints

**Why it matters:** Maps turn positional data into named data. That is what makes for_each and module inputs readable: the key documents what the value is for.

**What to do:** Create a local map named instance_types with dev and prod keys. The outputs show both a single-key lookup and the whole map.

**When to use it:** Use a map when each item has a meaningful name, when the order should not matter, or when you want stable keys for for_each.

**How to approach it:** Inside `locals`, add `instance_types = { ... }` with `dev` and `prod` keys. Keep the keys unquoted because they are valid identifiers, and quote the instance-size values. The outputs already look up `local.instance_types["dev"]` and the whole map, so keep the local name `instance_types`.


## Constraints

- Define local.instance_types as a map with dev and prod keys.
- Use a small instance size for dev and a larger one for prod.
- Output dev_instance_type with local.instance_types["dev"].

## Input variables

| Name | Type | Default |
| --- | --- | --- |

## Expected resources

- (see constraints)

## Expected outputs

- `dev_instance_type`
- `all_instance_types`

## How to test

```powershell
python judge.py test 18 --dir workspaces/018-tut-map-first
```

> Hidden test details are only revealed after a submission.
