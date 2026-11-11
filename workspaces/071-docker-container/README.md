# 071 - Run an Nginx Container

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
python judge.py test 71 --dir workspaces/071-docker-container
```

> Hidden test details are only revealed after a submission.
