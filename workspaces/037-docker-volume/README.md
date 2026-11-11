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

**What to do:** Complete the marked TODO in `main.tf`. Add the arguments and nested blocks required for docker_volume. Use the visible constraints as your checklist before you run the tests.

**When to use it:** Use local container resources for practice and integration tests, not as a replacement for production orchestration.

**How to approach it:** Open `main.tf` and work inside the single TODO region. Change one requirement at a time: add the named block, argument or reference, then run the tests. When a check fails, match its wording to the constraints and fix only the block it names.


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
