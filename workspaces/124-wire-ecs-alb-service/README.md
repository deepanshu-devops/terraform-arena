# 124 - ECS Fargate Service Behind an ALB

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

## Hints

**Why it matters:** Container services need a cluster, task definition and service wiring. Codifying them makes image and capacity changes reviewable.

**What to do:** Complete the marked region in `main.tf`. The work is inside `resource "aws_ecs_service" "this"`. Add the arguments and nested blocks required for aws_ecs_service. Use the visible constraints as the checklist for names, values and references before you run the tests.

**When to use it:** Use ECS when you want managed container orchestration without adopting Kubernetes.

**How to approach it:** Open `main.tf` and work only inside `resource "aws_ecs_service" "this"`. Use this code shape: name; desired_count; launch_type; cluster; task_definition; network_configuration { subnets; security_groups }. Use the already-declared references instead of hardcoded values: `aws_ecs_cluster.this.id`, `aws_ecs_task_definition.this.arn`, `var.subnet_ids`, `var.security_group_ids`. Keep the block header and braces, indent nested blocks by two spaces, and add one argument or nested block at a time. Run the tests after each small change so the first failure points at the next name to fix.


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
python judge.py test 124 --dir workspaces/124-wire-ecs-alb-service
```

> Hidden test details are only revealed after a submission.
