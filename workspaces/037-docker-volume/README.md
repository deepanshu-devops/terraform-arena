# 037 - Create a Docker Volume

**Level:** Level 2 - First Resources  
**Difficulty:** Easy  
**Points:** 40  
**Tags:** docker, sandbox, storage

## Scenario

Create a named volume for persistent container data.

## What to complete

- File: `main.tf`
- Task: Complete the docker_volume resource
- Add the arguments and nested blocks required for docker_volume.

## Hints

**Why it matters:** The Docker provider gives a fast local sandbox for learning Terraform's resource lifecycle without cloud credentials.

**What to do:** Complete the marked region in `main.tf`. The work is inside `resource "docker_volume" "this"`. Add the arguments and nested blocks required for docker_volume. Use the visible constraints as the checklist for names, values and references before you run the tests.

**When to use it:** Use local container resources for practice and integration tests, not as a replacement for production orchestration.

**How to approach it:** Open `main.tf` and work only inside `resource "docker_volume" "this"`. Use this code shape: name. Use the already-declared references instead of hardcoded values: `var.volume_name`. Keep the block header and braces, indent nested blocks by two spaces, and add one argument or nested block at a time. Run the tests after each small change so the first failure points at the next name to fix.


## Constraints

- Declare the docker provider.
- docker_volume name from var.volume_name.
- Export volume_id.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `volume_name` | `string` | `app-data` |

## Expected resources

- `docker_volume`

## Expected outputs

- `volume_id`

## How to test

```powershell
python judge.py test 37 --dir workspaces/037-docker-volume
```

> Hidden test details are only revealed after a submission.
