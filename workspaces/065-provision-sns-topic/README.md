# 065 - Provision SNS Topic

**Level:** Level 2 - First Resources  
**Difficulty:** Easy  
**Points:** 50  
**Tags:** aws, sns, provisioning

## Scenario

Your platform team needs SNS Topic for a pub/sub fan-out topic. Write a reusable Terraform configuration that provisions it, drives every input through variables, applies the standard tags, and exports the operational identifiers.

## What to complete

- File: `main.tf`
- Task: Complete the aws_sns_topic resource
- Add the arguments and nested blocks required for aws_sns_topic.

## Constraints

- Provider: aws (region from var.aws_region).
- Create exactly one resource of type aws_sns_topic.
- All configurable values must come from variables declared in variables.tf.
- No hardcoded AWS credentials.
- Code must pass terraform fmt conventions (2-space indents, trailing newline, no tabs).
- Tag the resource with Project, Environment and ManagedBy = "terraform".
- Expose outputs: topic_arn.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `topic_name` | `string` | `alerts` |
| `environment` | `string` | `dev` |
| `project_name` | `string` | `terraform-practice` |
| `aws_region` | `string` | `us-east-1` |

## Expected resources

- `aws_sns_topic`

## Expected outputs

- `topic_arn`

## How to test

```powershell
python judge.py test 65 --dir workspaces/065-provision-sns-topic
```

> Hidden test details are only revealed after a submission.
