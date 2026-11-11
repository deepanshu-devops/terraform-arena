# 028 - Pull a Docker Image

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
python judge.py test 28 --dir workspaces/028-docker-image
```

> Hidden test details are only revealed after a submission.
