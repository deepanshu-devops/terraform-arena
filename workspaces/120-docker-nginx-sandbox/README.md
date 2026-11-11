# 120 - Docker Nginx Sandbox

**Level:** Level 5 - Modules & Capstones  
**Difficulty:** Easy  
**Points:** 100  
**Tags:** docker, sandbox, providers, outputs

## Scenario

Before shipping AWS challenges to a live judge, you must prove the workflow on a zero-cost local sandbox. Using the Docker provider, provision an Nginx container that publishes port 80 on a configurable host port, restarts unless stopped, and carries operational labels. This challenge can be applied and destroyed against your local Docker daemon — no cloud bill.

## What to complete

- File: `main.tf`
- Task: Complete the Nginx container
- Wire the name, image, restart policy, published port and operational labels.

## Constraints

- Provider: kreuzwerker/docker declared in required_providers.
- Docker provider host must reference var.docker_host (default: npipe:////./pipe/docker_engine).
- container_name must be a validated lowercase/hyphen string.
- host_port must be a number defaulting to 8080 with validation 1024–65535.
- image_name must default to nginx:alpine.
- The container must publish internal port 80 on var.host_port.
- restart policy must be unless-stopped.
- privileged must be false; mounting docker.sock and host networking are blocked.
- Container must carry labels: Project, Environment, ManagedBy = "terraform".
- Outputs must expose container_id, container_name and url.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `docker_host` | `string` | `npipe:////./pipe/docker_engine` |
| `container_name` | `string` | `tf-arena-nginx` |
| `host_port` | `number` | `8080` |
| `image_name` | `string` | `nginx:alpine` |
| `project_name` | `string` | `terraform-practice` |
| `environment` | `string` | `dev` |

## Expected resources

- `docker_image`
- `docker_container`

## Expected outputs

- `container_id`
- `container_name`
- `url`

## How to test

```powershell
python judge.py test 120 --dir workspaces/120-docker-nginx-sandbox
```

> Hidden test details are only revealed after a submission.
