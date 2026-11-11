# 081 - Run an Nginx Container

**Level:** Level 2 - First Resources  
**Difficulty:** Easy  
**Points:** 55  
**Tags:** docker, sandbox

## Scenario

Run an Nginx container that publishes port 80 on a configurable host port.

## What to complete

- File: `main.tf`
- Task: Complete the docker_container resource
- Add the arguments and nested blocks required for docker_container.

## Hints

**Why it matters:** The Docker provider gives a fast local sandbox for learning Terraform's resource lifecycle without cloud credentials.

**What to do:** Complete the marked region in `main.tf`. The work is inside `resource "docker_container" "this"`. Add the arguments and nested blocks required for docker_container. Use the visible constraints as the checklist for names, values and references before you run the tests.

**When to use it:** Use local container resources for practice and integration tests, not as a replacement for production orchestration.

**How to approach it:** Open `main.tf` and work only inside `resource "docker_container" "this"`. Use this code shape: name; image; ports { internal; external }; ports {}. Use the already-declared references instead of hardcoded values: `var.container_name`, `var.image`. Keep the block header and braces, indent nested blocks by two spaces, and add one argument or nested block at a time. Run the tests after each small change so the first failure points at the next name to fix.


## Constraints

- Declare the docker provider.
- Container image from var.image.
- Ports block maps 80 -> var.host_port.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `container_name` | `string` | `web` |
| `image` | `string` | `nginx:alpine` |
| `host_port` | `number` | `8080` |

## Expected resources

- `docker_container`

## Expected outputs

- `container_id`

## How to test

```powershell
python judge.py test 81 --dir workspaces/081-docker-container
```

> Hidden test details are only revealed after a submission.
