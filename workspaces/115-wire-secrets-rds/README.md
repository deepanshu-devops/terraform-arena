# 115 - Secrets Manager + RDS

**Level:** Level 4 - Composition  
**Difficulty:** Hard  
**Points:** 120  
**Tags:** aws, secretsmanager, rds, security

## Scenario

Store database credentials in Secrets Manager and make sure the database is encrypted and private.

## What to complete

- File: `main.tf`
- Task: Complete the aws_db_instance resource
- Add the arguments and nested blocks required for aws_db_instance.

## Hints

**Why it matters:** Secrets should live in a managed secret store, not in code or state. Rotation and access policy are easier to audit there.

**What to do:** Complete the marked region in `main.tf`. The work is inside `resource "aws_db_instance" "this"`. Add the arguments and nested blocks required for aws_db_instance. Use the visible constraints as the checklist for names, values and references before you run the tests.

**When to use it:** Use a secret store for credentials and API keys that applications read at runtime.

**How to approach it:** Open `main.tf` and work only inside `resource "aws_db_instance" "this"`. Use this code shape: identifier; engine; engine_version; instance_class; allocated_storage; skip_final_snapshot; storage_encrypted; publicly_accessible; tags. Use the already-declared references instead of hardcoded values: `aws_secretsmanager_secret.this.arn`. Keep the block header and braces, indent nested blocks by two spaces, and add one argument or nested block at a time. Run the tests after each small change so the first failure points at the next name to fix.


## Constraints

- Create a Secrets Manager secret.
- Instance is encrypted and not public.
- No hardcoded credentials.

## Input variables

| Name | Type | Default |
| --- | --- | --- |
| `secret_name` | `string` | `app/db` |
| `db_engine` | `string` | `postgres` |
| `db_name` | `string` | `appdb` |
| `db_username` | `string` | `appuser` |
| `db_password` | `string` | `required` |
| `project_name` | `string` | `terraform-practice` |
| `environment` | `string` | `dev` |
| `aws_region` | `string` | `us-east-1` |

## Expected resources

- `aws_secretsmanager_secret`
- `aws_db_instance`

## Expected outputs

- `secret_arn`
- `db_endpoint`

## How to test

```powershell
python judge.py test 115 --dir workspaces/115-wire-secrets-rds
```

> Hidden test details are only revealed after a submission.
