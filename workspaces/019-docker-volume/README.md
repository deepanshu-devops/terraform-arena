# 019 - Create a Docker Volume

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
python judge.py test 19 --dir workspaces/019-docker-volume
```

> Hidden test details are only revealed after a submission.
