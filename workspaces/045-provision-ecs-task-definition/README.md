# 045 - Provision ECS Task Definition

**Level:** Level 2 - First Resources  
**Difficulty:** Easy  
**Points:** 50  
**Tags:** aws, ecs, provisioning

## Scenario

Your platform team needs ECS Task Definition for a small Fargate task blueprint. Write a reusable Terraform configuration that provisions it, drives every input through variables, applies the standard tags, and exports the operational identifiers.

## What to complete

- File: `main.tf`
- Task: Complete the aws_ecs_task_definition resource
- Add the arguments and nested blocks required for aws_ecs_task_definition.

## Constraints

- Provider: aws (region from var.aws_region).
- Create exactly one resource of type aws_ecs_task_definition.
- All configurable values must come from variables declared in variables.tf.
- No hardcoded AWS credentials.
- Code must pass terraform fmt conventions (2-space indents, trailing newline, no tabs).
- Expose outputs: task_definition_arn.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `family` | `string` | `app-task` |
| `container_image` | `string` | `nginx:alpine` |
| `aws_region` | `string` | `us-east-1` |

## Expected resources

- `aws_ecs_task_definition`

## Expected outputs

- `task_definition_arn`

## How to test

```powershell
python judge.py test 45 --dir workspaces/045-provision-ecs-task-definition
```

> Hidden test details are only revealed after a submission.
