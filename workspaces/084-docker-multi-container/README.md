# 084 - Two Containers on One Network

**Level:** Level 3 - Real Infrastructure  
**Difficulty:** Medium  
**Points:** 80  
**Tags:** docker, sandbox, networking

## Scenario

Run two containers attached to the same user-defined Docker network.

## What to complete

- File: `main.tf`
- Task: Complete the shared Docker network
- Create the network that both containers join.

## Constraints

- Create a network.
- Create two containers attached to it.
- Use distinct names.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `network_name` | `string` | `app-net` |

## Expected resources

- `docker_network`
- `docker_container`

## Expected outputs

- `network_id`

## How to test

```powershell
python judge.py test 84 --dir workspaces/084-docker-multi-container
```

> Hidden test details are only revealed after a submission.
