# 036 - Create a Docker Network

**Level:** Level 2 - First Resources  
**Difficulty:** Easy  
**Points:** 40  
**Tags:** docker, sandbox, networking

## Scenario

Create an isolated bridge network for containers.

## What to complete

- File: `main.tf`
- Task: Complete the docker_network resource
- Add the arguments and nested blocks required for docker_network.

## Hints

**Why it matters:** The Docker provider gives a fast local sandbox for learning Terraform's resource lifecycle without cloud credentials.

**What to do:** Complete the marked TODO in `main.tf`. Add the arguments and nested blocks required for docker_network. Use the visible constraints as your checklist before you run the tests.

**When to use it:** Use local container resources for practice and integration tests, not as a replacement for production orchestration.

**How to approach it:** Open `main.tf` and work inside the single TODO region. Change one requirement at a time: add the named block, argument or reference, then run the tests. When a check fails, match its wording to the constraints and fix only the block it names.


## Constraints

- Declare the docker provider.
- docker_network name from var.network_name.
- Export network_id.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `network_name` | `string` | `app-net` |

## Expected resources

- `docker_network`

## Expected outputs

- `network_id`

## How to test

```powershell
python judge.py test 36 --dir workspaces/036-docker-network
```

> Hidden test details are only revealed after a submission.
