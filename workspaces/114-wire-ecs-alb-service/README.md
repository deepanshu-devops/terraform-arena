# 114 - ECS Fargate Service Behind an ALB

**Level:** Level 4 - Composition  
**Difficulty:** Hard  
**Points:** 160  
**Tags:** aws, ecs, fargate, alb, containers

## Scenario

Run a small Fargate service and register it with an ALB target group on port 80.

## What to complete

- File: `main.tf`
- Task: Complete the aws_ecs_service resource
- Add the arguments and nested blocks required for aws_ecs_service.

## Constraints

- Create cluster, task definition and service.
- Task uses Fargate/awsvpc and small CPU/memory.
- Service registers with the target group.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `cluster_name` | `string` | `app-cluster` |
| `family` | `string` | `app-task` |
| `container_image` | `string` | `nginx:alpine` |
| `vpc_id` | `string` | `required` |
| `subnet_ids` | `list(string)` | `required` |
| `security_group_ids` | `list(string)` | `required` |
| `project_name` | `string` | `terraform-practice` |
| `environment` | `string` | `dev` |
| `aws_region` | `string` | `us-east-1` |

## Expected resources

- `aws_ecs_cluster`
- `aws_ecs_task_definition`
- `aws_ecs_service`
- `aws_lb`
- `aws_lb_target_group`
- `aws_lb_listener`

## Expected outputs

- `cluster_arn`
- `service_name`

## How to test

```powershell
python judge.py test 114 --dir workspaces/114-wire-ecs-alb-service
```

> Hidden test details are only revealed after a submission.
