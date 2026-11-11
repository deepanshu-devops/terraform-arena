# 069 - Provision Route 53 Hosted Zone

**Level:** Level 2 - First Resources  
**Difficulty:** Easy  
**Points:** 50  
**Tags:** aws, route53, provisioning

## Scenario

Your platform team needs Route 53 Hosted Zone for authoritative DNS for a domain. Write a reusable Terraform configuration that provisions it, drives every input through variables, applies the standard tags, and exports the operational identifiers.

## What to complete

- File: `main.tf`
- Task: Complete the aws_route53_zone resource
- Add the arguments and nested blocks required for aws_route53_zone.

## Hints

**Why it matters:** DNS is the public name of the system. Managing records in Terraform keeps the name, certificate and endpoint changes together.

**What to do:** Complete the marked region in `main.tf`. The work is inside `resource "aws_route53_zone" "this"`. Add the arguments and nested blocks required for aws_route53_zone. Use the visible constraints as the checklist for names, values and references before you run the tests.

**When to use it:** Use Route 53 when a service needs a stable hostname or when DNS changes should be reviewed with the rest of the stack.

**How to approach it:** Open `main.tf` and work only inside `resource "aws_route53_zone" "this"`. Use this code shape: name; tags. Use the already-declared references instead of hardcoded values: `var.domain_name`, `var.project_name`, `var.environment`. Keep the block header and braces, indent nested blocks by two spaces, and add one argument or nested block at a time. Run the tests after each small change so the first failure points at the next name to fix.


## Constraints

- Provider: aws (region from var.aws_region).
- Create exactly one resource of type aws_route53_zone.
- All configurable values must come from variables declared in variables.tf.
- No hardcoded AWS credentials.
- Code must pass terraform fmt conventions (2-space indents, trailing newline, no tabs).
- Tag the resource with Project, Environment and ManagedBy = "terraform".
- Expose outputs: zone_id.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `domain_name` | `string` | `example.com` |
| `environment` | `string` | `dev` |
| `project_name` | `string` | `terraform-practice` |
| `aws_region` | `string` | `us-east-1` |

## Expected resources

- `aws_route53_zone`

## Expected outputs

- `zone_id`

## How to test

```powershell
python judge.py test 69 --dir workspaces/069-provision-route53-zone
```

> Hidden test details are only revealed after a submission.
