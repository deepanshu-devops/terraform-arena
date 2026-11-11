# 018 - Create a Docker Network

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
python judge.py test 18 --dir workspaces/018-docker-network
```

> Hidden test details are only revealed after a submission.
