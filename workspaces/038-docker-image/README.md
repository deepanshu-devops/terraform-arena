# 038 - Pull a Docker Image

**Level:** Level 2 - First Resources  
**Difficulty:** Easy  
**Points:** 45  
**Tags:** docker, sandbox

## Scenario

Use the Docker provider to pull nginx:alpine as a managed image.

## What to complete

- File: `main.tf`
- Task: Complete the docker_image resource
- Add the arguments and nested blocks required for docker_image.

## Hints

**Why it matters:** The Docker provider gives a fast local sandbox for learning Terraform's resource lifecycle without cloud credentials.

**What to do:** Complete the marked region in `main.tf`. The work is inside `resource "docker_image" "this"`. Add the arguments and nested blocks required for docker_image. Use the visible constraints as the checklist for names, values and references before you run the tests.

**When to use it:** Use local container resources for practice and integration tests, not as a replacement for production orchestration.

**How to approach it:** Open `main.tf` and work only inside `resource "docker_image" "this"`. Use this code shape: name. Use the already-declared references instead of hardcoded values: `var.image_name`. Keep the block header and braces, indent nested blocks by two spaces, and add one argument or nested block at a time. Run the tests after each small change so the first failure points at the next name to fix.


## Constraints

- Declare the docker provider.
- docker_image name from var.image_name.
- Export image_id.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `image_name` | `string` | `nginx:alpine` |

## Expected resources

- `docker_image`

## Expected outputs

- `image_id`

## How to test

```powershell
python judge.py test 38 --dir workspaces/038-docker-image
```

> Hidden test details are only revealed after a submission.
