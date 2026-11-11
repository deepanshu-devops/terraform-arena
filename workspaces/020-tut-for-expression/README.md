# 020 - Tutorial: Transform a List With for

**Level:** Level 0 - HCL Foundations  
**Difficulty:** Easy  
**Points:** 68  
**Tags:** terraform, tutorial, expressions, collections

## Scenario

A for expression builds a new collection from an existing one. Use it to turn a list of team names into uppercase labels and a map of owners, without writing each entry twice.

## What to complete

- File: `main.tf`
- Task: Derive the collections
- Create the source list, then transform it into a list and a map.

## Hints

**Why it matters:** for expressions are the bridge between a plain collection and the shape a resource or module needs. They remove the copy-paste step that causes drift.

**What to do:** Create one source list and two derived locals. One derived value is a list of uppercase names; the other is a map from each name to an owner string.

**When to use it:** Use a for expression when you need to transform every item in a collection. Use a map comprehension when each result needs a key.

**How to approach it:** Start with `teams` as a list. Build `upper_teams` with a bracketed `for` expression over `local.teams` and apply the uppercase function to the loop variable. Build `team_owners` with a braced `for` expression that maps each team name to its owner string using an arrow. Keep the three local names the outputs expect.


## Constraints

- Define local.teams with platform and security.
- Use a for expression to build local.upper_teams.
- Use a for expression to build local.team_owners.
- Export both derived collections.

## Input variables

| Name | Type | Default |
| --- | --- | --- |

## Expected resources

- (see constraints)

## Expected outputs

- `upper_teams`
- `team_owners`

## How to test

```powershell
python judge.py test 20 --dir workspaces/020-tut-for-expression
```

> Hidden test details are only revealed after a submission.
