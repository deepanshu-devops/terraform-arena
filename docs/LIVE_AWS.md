# Live AWS pilot (explicitly gated)

The default app is **offline and static**. `judge.py live` is an opt-in
validation layer that plans, applies, and destroys a small allowlisted set of
challenges in a **dedicated sandbox AWS account**.

It is intentionally conservative. A run is blocked before `apply` if the plan
contains a billable, destructive, or deliberately insecure resource.

---

## 1. Do not put AWS keys in this repo or in chat

Use a local AWS profile. The credentials stay in
`%USERPROFILE%\.aws\credentials`, outside the project.

```powershell
aws configure --profile tf-arena-sandbox
# Access key ID:     paste at the prompt only
# Secret access key: paste at the prompt only
# Default region:    us-east-1
# Output format:     json

aws sts get-caller-identity --profile tf-arena-sandbox
```

Use a dedicated sandbox account, not production. Root credentials are refused.
Prefer an IAM role or SSO profile with only the permissions needed for the
pilot resources (VPC, SQS, CloudWatch Logs). Do not use `AdministratorAccess`
unless this is a disposable account and you accept the risk.

Set a small AWS Budget alarm (for example, $1–$5) before applying anything.

---

## 2. Install Terraform

```powershell
powershell -ExecutionPolicy Bypass -File scripts\install_terraform.ps1
$env:Path = "$PWD\tools\terraform;$env:Path"
terraform version
```

The runner also finds `tools\terraform\terraform.exe` directly.

---

## 3. Configure the gates

```powershell
$env:ARENA_LIVE = "1"
$env:ARENA_LIVE_PROFILE = "tf-arena-sandbox"
$env:ARENA_LIVE_ACCOUNT = "123456789012"   # your sandbox account id
$env:ARENA_LIVE_REGION = "us-east-1"
```

`ARENA_LIVE_ACCOUNT` is mandatory and is compared with
`aws sts get-caller-identity`. This prevents accidentally running in the wrong
account. Only `us-east-1` is allowlisted in the first pilot.

Check the non-network status:

```powershell
python judge.py live --status
```

Check the actual identity and all gates:

```powershell
python judge.py live --preflight
```

---

## 4. Pilot challenges

The allowlist is keyed by stable challenge id, not by display number, so catalog
renumbering cannot change which scenarios are permitted live.

| # | Stable id | Challenge | Resources | Cost note |
| --- | --- | --- | --- | --- |
| 061 | `provision-vpc` | Provision VPC | `aws_vpc` | VPCs are free |
| 069 | `provision-sqs-queue` | Provision SQS Queue | `aws_sqs_queue` | Queue creation is free; pilot sends no messages |
| 031 | `provision-log-group` | Provision CloudWatch Log Group | `aws_cloudwatch_log_group` | Log group creation is free; pilot writes no logs |

Those numbers reflect the current level-ordered catalog. The ids are authoritative.

The workspace starters are incomplete. Fill in the focus block and get a static
PASS first:

```powershell
python judge.py test provision-vpc
python judge.py test provision-sqs-queue
python judge.py test provision-log-group
```

If you need to supply required values, use a tfvars file:

```powershell
python judge.py live provision-vpc --var-file .\my-live.tfvars
```

The runner always overrides `project_name`, `aws_region`, and known name
variables with a unique run-scoped value, so resources are easy to identify and
clean up.

---

## 5. Plan first, then apply

Plan-only (default, creates nothing):

```powershell
python judge.py live provision-vpc
```

Apply and destroy (requires both gates):

```powershell
$env:ARENA_LIVE_APPLY = "1"
python judge.py live provision-vpc --apply --yes
```

`--apply` alone is not enough: the environment gate and `--yes` are both
required.

---

## 6. What the runner does

1. Resolves the AWS identity and verifies the sandbox account id.
2. Copies the challenge workspace to `data/live/` (state and `.terraform` are
   never copied).
3. Rejects remote backends, `prevent_destroy`, provisioners, external data
   sources, hard-coded credentials, and IAM identity resources.
4. Runs `terraform init -backend=false`, `terraform validate`, and `terraform
   plan -out=arena.tfplan`.
5. Inspects the plan JSON and allows only clean creates of allowlisted types.
6. Applies the exact reviewed plan.
7. Captures outputs and state.
8. Always runs `terraform destroy` in a `finally` block.
9. Verifies the state is empty and sweeps for leftovers by the unique
   `Project` tag and name prefixes.
10. Keeps `data/live/<run>` for inspection if cleanup is incomplete.

### Blocked before apply

- Any `update`, `delete`, or `replace` action
- `aws_nat_gateway`, `aws_eip`, `aws_lb`/ALB, `aws_instance`,
  `aws_autoscaling_group`, `aws_ebs_volume`, `aws_efs_file_system`
- `aws_db_instance`, `aws_rds_cluster`, `aws_ecs_*`, `aws_eks_*`
- `aws_route53_*`, `aws_cloudfront_*`, `aws_acm_*`, `aws_wafv2_*`
- `aws_kms_*`, `aws_secretsmanager_*`, `aws_ecr_*`
- IAM users/access keys/roles/policies
- S3 buckets without a public access block, public ACLs, public bucket policies
- Security-group ingress from `0.0.0.0/0` or `::/0`
- DynamoDB provisioned capacity or deletion protection
- NAT/Transit Gateway routes
- Remote backends and `prevent_destroy`

---

## 7. If cleanup fails

Do **not** delete the `data/live/` folder first. Inspect the report:

```powershell
python judge.py live provision-vpc --apply --yes --json
```

The report includes `destroy`, `state_after_destroy`, `sweep.residual`, and the
kept `workdir`. Re-run destroy from that directory with the same profile and
region:

```powershell
cd data\live\arena-live-061-...
$env:AWS_PROFILE = "tf-arena-sandbox"
$env:AWS_REGION = "us-east-1"
..\..\tools\terraform\terraform.exe destroy -auto-approve
```

If resources are still listed, remove them manually only after confirming they
carry the run's `Project = arena-<run-id>` tag.

The sweep is a safety net, not a license to run unattended. Stay at the
keyboard for apply/destroy.

---

## 8. Why the other 114 challenges are not live yet

Many are intentionally expensive or insecure:

- NAT Gateway, ALB, EIP, RDS, ECS/Fargate, CloudFront, Route 53, WAF, KMS
- public S3 buckets and `0.0.0.0/0` security groups
- `prevent_destroy` lifecycle exercises
- remote state/backend exercises
- Docker challenges that need a local Docker engine, not AWS

Those stay static-only (or plan-only) until a separate sandbox design, budget,
and cleanup policy exists.
