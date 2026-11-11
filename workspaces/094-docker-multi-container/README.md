# 094 - Two Containers on One Network

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

## Hints

**Why it matters:** The Docker provider gives a fast local sandbox for learning Terraform's resource lifecycle without cloud credentials.

**What to do:** Complete the marked TODO in `main.tf`. Create the network that both containers join. Use the visible constraints as your checklist before you run the tests.

**When to use it:** Use local container resources for practice and integration tests, not as a replacement for production orchestration.

**How to approach it:** Open `main.tf` and work inside the single TODO region. Change one requirement at a time: add the named block, argument or reference, then run the tests. When a check fails, match its wording to the constraints and fix only the block it names.


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
python judge.py test 94 --dir workspaces/094-docker-multi-container
```

> Hidden test details are only revealed after a submission.
