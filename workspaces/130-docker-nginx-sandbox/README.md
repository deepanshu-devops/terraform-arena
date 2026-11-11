# 130 - Docker Nginx Sandbox

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

## Hints

**Why it matters:** Providers tell Terraform which API to call and how to authenticate. Pinning the provider and keeping settings in variables makes a configuration portable and reproducible.

**What to do:** Complete the marked region in `main.tf`. The work is inside `resource "docker_container" "this"`. Wire the name, image, restart policy, published port and operational labels. Use the visible constraints as the checklist for names, values and references before you run the tests.

**When to use it:** Configure a provider once per module and pass credentials through the environment or a secure mechanism, never through committed literals.

**How to approach it:** Open `main.tf` and work only inside `resource "docker_container" "this"`. Use this code shape: name; image; restart; ports { internal; external }; labels { label; value } x3. Use the already-declared references instead of hardcoded values: `var.container_name`, `docker_image.this.image_id`, `var.host_port`, `var.project_name`, `var.environment`. Keep the block header and braces, indent nested blocks by two spaces, and add one argument or nested block at a time. Run the tests after each small change so the first failure points at the next name to fix.


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
python judge.py test 130 --dir workspaces/130-docker-nginx-sandbox
```

> Hidden test details are only revealed after a submission.
