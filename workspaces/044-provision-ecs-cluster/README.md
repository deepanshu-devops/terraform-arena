# 044 - Provision ECS Cluster

**Level:** Level 2 - First Resources  
**Difficulty:** Easy  
**Points:** 50  
**Tags:** aws, ecs, provisioning

## Scenario

Your platform team needs ECS Cluster for a logical boundary for container services. Write a reusable Terraform configuration that provisions it, drives every input through variables, applies the standard tags, and exports the operational identifiers.

## What to complete

- File: `main.tf`
- Task: Complete the aws_ecs_cluster resource
- Add the arguments and nested blocks required for aws_ecs_cluster.

## Constraints

- Provider: aws (region from var.aws_region).
- Create exactly one resource of type aws_ecs_cluster.
- All configurable values must come from variables declared in variables.tf.
- No hardcoded AWS credentials.
- Code must pass terraform fmt conventions (2-space indents, trailing newline, no tabs).
- Tag the resource with Project, Environment and ManagedBy = "terraform".
- Expose outputs: cluster_arn.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `cluster_name` | `string` | `app-cluster` |
| `environment` | `string` | `dev` |
| `project_name` | `string` | `terraform-practice` |
| `aws_region` | `string` | `us-east-1` |

## Expected resources

- `aws_ecs_cluster`

## Expected outputs

- `cluster_arn`

## How to test

```powershell
python judge.py test 44 --dir workspaces/044-provision-ecs-cluster
```

> Hidden test details are only revealed after a submission.
