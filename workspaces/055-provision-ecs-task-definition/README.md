# 055 - Provision ECS Task Definition

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

## Hints

**Why it matters:** Container services need a cluster, task definition and service wiring. Codifying them makes image and capacity changes reviewable.

**What to do:** Complete the marked region in `main.tf`. The work is inside `resource "aws_ecs_task_definition" "this"`. Add the arguments and nested blocks required for aws_ecs_task_definition. Use the visible constraints as the checklist for names, values and references before you run the tests.

**When to use it:** Use ECS when you want managed container orchestration without adopting Kubernetes.

**How to approach it:** Open `main.tf` and work only inside `resource "aws_ecs_task_definition" "this"`. Use this code shape: family; cpu; memory; network_mode; requires_compatibilities; container_definitions. Use the already-declared references instead of hardcoded values: `var.family`. Keep the block header and braces, indent nested blocks by two spaces, and add one argument or nested block at a time. Run the tests after each small change so the first failure points at the next name to fix.


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
python judge.py test 55 --dir workspaces/055-provision-ecs-task-definition
```

> Hidden test details are only revealed after a submission.
