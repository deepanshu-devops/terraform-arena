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

**What to do:** Complete the marked region in `main.tf`. The work is inside `resource "docker_network" "this"`. Add the arguments and nested blocks required for docker_network. Use the visible constraints as the checklist for names, values and references before you run the tests.

**When to use it:** Use local container resources for practice and integration tests, not as a replacement for production orchestration.

**How to approach it:** Open `main.tf` and work only inside `resource "docker_network" "this"`. Use this code shape: name. Use the already-declared references instead of hardcoded values: `var.network_name`. Keep the block header and braces, indent nested blocks by two spaces, and add one argument or nested block at a time. Run the tests after each small change so the first failure points at the next name to fix.


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
