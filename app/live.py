"""Explicitly gated live AWS validation.

The default application never calls AWS. This module is only reachable through
the ``judge.py live`` command and requires *all* of the following:

* ``ARENA_LIVE=1``
* a dedicated sandbox account id in ``ARENA_LIVE_ACCOUNT`` (or ``--account``)
* a profile that resolves to that account (``ARENA_LIVE_PROFILE`` or
  ``--profile``); long-lived keys must never be committed to this repo
* for apply: ``ARENA_LIVE_APPLY=1`` *and* ``--apply --yes``
* a challenge in the small pilot allowlist (VPC, SQS, CloudWatch Logs)

Every run is isolated in ``data/live/``. The runner plans first, inspects the
plan JSON against a strict resource/security allowlist, applies only that plan,
and destroys in a ``finally`` block. Destructive/update actions, billable
resource types, public buckets, open security groups, IAM/KMS/RDS/ECS/NAT/ALB
resources, remote backends, hard-coded credentials and ``prevent_destroy`` are
rejected before apply.
"""
from __future__ import annotations

import ipaddress
import json
import os
import re
import secrets
import shutil
import subprocess
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .evaluator import Challenge, evaluate
from .workspace import read_workspace, workspace_dir

ROOT = Path(__file__).resolve().parent.parent
LIVE_TEMP = ROOT / "data" / "live"
LOCAL_TERRAFORM = ROOT / "tools" / "terraform" / "terraform.exe"

# Deliberately tiny first pilot, keyed by stable challenge id rather than by
# display number so catalog reordering cannot silently change what is live.
PILOT_CHALLENGES = {"provision-vpc", "provision-sqs-queue", "provision-log-group"}
DEFAULT_REGION = "us-east-1"
ALLOWED_REGIONS = {"us-east-1"}

# Managed cloud resources that are cheap and safe enough for the pilot. The
# plan guard rejects everything else before apply. Data sources are ignored.
LIVE_ALLOWED_TYPES = {
    "aws_vpc",
    "aws_subnet",
    "aws_internet_gateway",
    "aws_route_table",
    "aws_route",
    "aws_route_table_association",
    "aws_security_group",
    "aws_security_group_rule",
    "aws_s3_bucket",
    "aws_s3_bucket_versioning",
    "aws_s3_bucket_public_access_block",
    "aws_s3_bucket_server_side_encryption_configuration",
    "aws_s3_bucket_ownership_controls",
    "aws_s3_bucket_lifecycle_configuration",
    "aws_s3_bucket_policy",
    "aws_sqs_queue",
    "aws_sqs_queue_policy",
    "aws_cloudwatch_log_group",
    "aws_cloudwatch_metric_alarm",
    "aws_dynamodb_table",
    "aws_sns_topic",
    "aws_sns_topic_subscription",
    "aws_cloudwatch_event_rule",
    "aws_cloudwatch_event_target",
    "aws_events_rule",
    "aws_events_target",
}

# Local-only providers. They create no cloud resources and are safe to allow.
LOCAL_PREFIXES = ("random_", "time_", "tls_")
LOCAL_TYPES = {"terraform_data", "null_resource"}

NAME_OVERRIDES = {
    "bucket_name": lambda base, run_id: f"{base}-bucket",
    "queue_name": lambda base, run_id: f"{base}-jobs",
    "log_group_name": lambda base, run_id: f"/arena/{run_id}/logs",
    "security_group_name": lambda base, run_id: f"{base}-sg",
    "web_acl_name": lambda base, run_id: f"{base}-waf",
    "topic_name": lambda base, run_id: f"{base}-topic",
    "table_name": lambda base, run_id: f"{base}-table",
    "function_name": lambda base, run_id: f"{base}-fn",
    "role_name": lambda base, run_id: f"{base}-role",
    "policy_name": lambda base, run_id: f"{base}-policy",
    "cluster_name": lambda base, run_id: f"{base}-cluster",
    "service_name": lambda base, run_id: f"{base}-svc",
    "repository_name": lambda base, run_id: f"{base}-repo",
    "secret_name": lambda base, run_id: f"{base}-secret",
    "key_alias": lambda base, run_id: f"alias/{base}",
}

SENSITIVE_WORDS = ("password", "secret", "token", "access_key", "private_key")


class LiveError(RuntimeError):
    """Raised when a live run is blocked before it can touch AWS."""


def enabled() -> bool:
    return os.environ.get("ARENA_LIVE", "0") == "1"


def apply_gate() -> bool:
    return os.environ.get("ARENA_LIVE_APPLY", "0") == "1"


def terraform_binary() -> str | None:
    if LOCAL_TERRAFORM.exists():
        return str(LOCAL_TERRAFORM)
    return shutil.which("terraform")


def status() -> dict[str, Any]:
    """Non-network status for the API and CLI. Never calls AWS."""
    return {
        "enabled": enabled(),
        "apply_gate": apply_gate(),
        "terraform": terraform_binary(),
        "aws_cli": shutil.which("aws"),
        "profile": os.environ.get("ARENA_LIVE_PROFILE")
        or os.environ.get("AWS_PROFILE")
        or "default",
        "region": os.environ.get("ARENA_LIVE_REGION")
        or os.environ.get("AWS_REGION")
        or DEFAULT_REGION,
        "account_configured": bool(os.environ.get("ARENA_LIVE_ACCOUNT")),
        "pilot_challenges": sorted(PILOT_CHALLENGES),
        "allowed_regions": sorted(ALLOWED_REGIONS),
        "allowed_types": sorted(LIVE_ALLOWED_TYPES),
    }


def _child_env(profile: str, region: str) -> dict[str, str]:
    """Build a clean child environment.

    Environment AWS keys are removed so the selected profile is authoritative.
    Terraform CLI argument/workspace overrides are removed to keep the run
    isolated and reproducible.
    """
    drop = {
        "AWS_ACCESS_KEY_ID",
        "AWS_SECRET_ACCESS_KEY",
        "AWS_SESSION_TOKEN",
        "AWS_SECURITY_TOKEN",
        "AWS_CREDENTIAL_EXPIRATION",
        "TF_WORKSPACE",
        "TF_DATA_DIR",
        "TF_LOG",
        "TF_LOG_PATH",
        "TF_LOG_PROVIDER",
        "TF_REATTACH_PROVIDERS",
    }
    env = {key: value for key, value in os.environ.items() if key not in drop}
    for key in list(env):
        if key.startswith("TF_CLI_ARGS"):
            env.pop(key, None)
    env.update(
        {
            "AWS_PROFILE": profile,
            "AWS_DEFAULT_PROFILE": profile,
            "AWS_REGION": region,
            "AWS_DEFAULT_REGION": region,
            "AWS_SDK_LOAD_CONFIG": "1",
            "AWS_EC2_METADATA_DISABLED": "true",
            "AWS_PAGER": "",
            "TF_IN_AUTOMATION": "1",
            "TF_INPUT": "0",
            "CHECKPOINT_DISABLE": "1",
        }
    )
    return env


def _run(
    cmd: list[str], cwd: Path, env: dict[str, str], timeout: int
) -> dict[str, Any]:
    started = time.monotonic()
    creationflags = getattr(subprocess, "CREATE_NO_WINDOW", 0) if os.name == "nt" else 0
    try:
        proc = subprocess.run(
            cmd,
            cwd=str(cwd),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
            env=env,
            creationflags=creationflags,
        )
        return {
            "ok": proc.returncode == 0,
            "code": proc.returncode,
            "stdout": proc.stdout or "",
            "stderr": proc.stderr or "",
            "duration_ms": int((time.monotonic() - started) * 1000),
        }
    except subprocess.TimeoutExpired as exc:
        stdout = exc.stdout or ""
        stderr = exc.stderr or ""
        if isinstance(stdout, bytes):
            stdout = stdout.decode("utf-8", "replace")
        if isinstance(stderr, bytes):
            stderr = stderr.decode("utf-8", "replace")
        return {
            "ok": False,
            "code": -1,
            "stdout": stdout,
            "stderr": f"timed out after {timeout}s\n{stderr}",
            "duration_ms": int((time.monotonic() - started) * 1000),
        }
    except Exception as exc:  # pragma: no cover - defensive
        return {
            "ok": False,
            "code": -1,
            "stdout": "",
            "stderr": f"{type(exc).__name__}: {exc}",
            "duration_ms": int((time.monotonic() - started) * 1000),
        }


def _slim(result: dict[str, Any], limit: int = 5000) -> dict[str, Any]:
    return {
        "ok": result.get("ok", False),
        "code": result.get("code"),
        "duration_ms": result.get("duration_ms", 0),
        "stdout": (result.get("stdout") or "")[-limit:],
        "stderr": (result.get("stderr") or "")[-limit:],
    }


def _aws(
    ctx: dict[str, Any], args: list[str], timeout: int = 60
) -> dict[str, Any]:
    return _run(
        [
            ctx["aws"],
            *args,
            "--profile",
            ctx["profile"],
            "--region",
            ctx["region"],
            "--output",
            "json",
            "--no-cli-pager",
        ],
        ROOT,
        ctx["env"],
        timeout,
    )


def _identity(ctx: dict[str, Any]) -> dict[str, Any]:
    result = _aws(ctx, ["sts", "get-caller-identity"], timeout=60)
    if not result["ok"]:
        detail = (result.get("stderr") or result.get("stdout") or "").strip()
        hint = ""
        if "ExpiredToken" in detail or "SSO" in detail or "sso" in detail:
            hint = f"\nHint: run `aws sso login --profile {ctx['profile']}`."
        raise LiveError(f"Could not resolve AWS identity.\n{detail}{hint}")
    try:
        return json.loads(result["stdout"] or "{}")
    except json.JSONDecodeError as exc:
        raise LiveError(f"AWS returned invalid identity JSON: {exc}") from exc


def preflight(
    profile: str | None = None,
    region: str | None = None,
    account: str | None = None,
    require_apply: bool = False,
) -> dict[str, Any]:
    if not enabled():
        raise LiveError(
            "Live AWS mode is disabled. Set ARENA_LIVE=1 to enable it."
        )
    tf = terraform_binary()
    if not tf:
        raise LiveError(
            "Terraform is not installed. Run scripts\\install_terraform.ps1 first."
        )
    aws = shutil.which("aws")
    if not aws:
        raise LiveError("AWS CLI is not installed or not on PATH.")

    profile = (
        profile
        or os.environ.get("ARENA_LIVE_PROFILE")
        or os.environ.get("AWS_PROFILE")
        or "default"
    )
    region = (
        region
        or os.environ.get("ARENA_LIVE_REGION")
        or os.environ.get("AWS_REGION")
        or DEFAULT_REGION
    )
    account = account or os.environ.get("ARENA_LIVE_ACCOUNT")

    if region not in ALLOWED_REGIONS:
        raise LiveError(
            f"Region {region!r} is not in the live allowlist "
            f"({', '.join(sorted(ALLOWED_REGIONS))})."
        )
    if not account:
        raise LiveError(
            "Set ARENA_LIVE_ACCOUNT to the dedicated sandbox account id. "
            "This prevents accidentally running against another account."
        )
    if not re.fullmatch(r"\d{12}", account):
        raise LiveError("ARENA_LIVE_ACCOUNT must be a 12-digit AWS account id.")
    if require_apply and not apply_gate():
        raise LiveError(
            "Apply is disabled. Set ARENA_LIVE_APPLY=1 and pass --apply --yes."
        )

    ctx = {
        "profile": profile,
        "region": region,
        "account": account,
        "aws": aws,
        "terraform": tf,
        "env": _child_env(profile, region),
    }
    identity = _identity(ctx)
    actual = str(identity.get("Account", ""))
    if actual != account:
        raise LiveError(
            f"Refusing to run: profile {profile!r} resolves to account {actual!r}, "
            f"not ARENA_LIVE_ACCOUNT={account!r}."
        )
    arn = str(identity.get("Arn", ""))
    if arn.endswith(":root"):
        raise LiveError(
            "Refusing to run with root credentials. Use a dedicated IAM user "
            "or role with least privilege in the sandbox account."
        )
    ctx["identity"] = identity
    return ctx


def new_run_id() -> str:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    return f"{stamp}-{secrets.token_hex(3)}"


def build_overrides(
    challenge: Challenge, region: str, run_id: str
) -> tuple[dict[str, Any], list[str], list[str]]:
    """Return (tfvars, missing_required, warnings)."""
    base = f"arena-{run_id}"
    overrides: dict[str, Any] = {}
    missing: list[str] = []
    warnings: list[str] = []

    for variable in challenge.variables:
        name = str(variable.get("name", ""))
        if not name:
            continue
        has_default = "default" in variable
        default = variable.get("default")

        if name == "aws_region":
            overrides[name] = region
        elif name == "project_name":
            overrides[name] = base
        elif name == "environment":
            if not has_default:
                overrides[name] = "dev"
        elif name == "availability_zone":
            overrides[name] = f"{region}a"
        elif name in NAME_OVERRIDES:
            overrides[name] = NAME_OVERRIDES[name](base, run_id)
            if variable.get("validation"):
                warnings.append(
                    f"{name} has a validation rule; the generated value may be rejected."
                )
        elif name == "db_password":
            overrides[name] = secrets.token_urlsafe(24)
        elif name == "db_username":
            overrides[name] = "arenaadmin"
        elif name == "db_name":
            overrides[name] = "arenadb"
        elif not has_default:
            missing.append(name)

    return overrides, missing, warnings


def _redact(values: dict[str, Any]) -> dict[str, Any]:
    clean: dict[str, Any] = {}
    for key, value in values.items():
        if any(word in key.lower() for word in SENSITIVE_WORDS):
            clean[key] = "***"
        else:
            clean[key] = value
    return clean


def _redact_outputs(outputs: dict[str, Any]) -> dict[str, Any]:
    clean: dict[str, Any] = {}
    for key, item in outputs.items():
        if isinstance(item, dict):
            copy = dict(item)
            if copy.get("sensitive"):
                copy["value"] = "***"
            clean[key] = copy
        else:
            clean[key] = item
    return clean


IGNORE = shutil.ignore_patterns(
    ".terraform",
    ".terraform.*",
    "*.tfstate",
    "*.tfstate.*",
    "*.tfplan",
    "arena.tfplan",
    "arena.auto.tfvars.json",
    "arena.user.tfvars",
    "crash.log",
    "README.md",
    "challenge.json",
    ".git",
    "node_modules",
    "__pycache__",
    "data",
    "tools",
)


def copy_workspace(challenge: Challenge, destination: Path) -> None:
    source = workspace_dir(challenge)
    if not source.exists():
        raise LiveError(
            f"Workspace not found: {source}. Run `python judge.py start {challenge.number}`."
        )
    if not list(source.glob("*.tf")):
        raise LiveError(
            f"No .tf files in {source}. Fill in the starter before a live run."
        )
    shutil.copytree(source, destination, dirs_exist_ok=True, ignore=IGNORE)


def check_workspace_safety(workdir: Path) -> list[str]:
    """Reject patterns that are unsafe or impossible to clean up."""
    warnings: list[str] = []
    patterns = [
        (re.compile(r"\bbackend\s+\""), "remote backend blocks are not supported in live mode"),
        (re.compile(r"prevent_destroy\s*=\s*true"), "prevent_destroy would block cleanup"),
        (re.compile(r"\bprovisioner\s+\"(?:local-exec|remote-exec)\""), "local/remote-exec provisioners are blocked"),
        (re.compile(r"\bdata\s+\"external\""), "external data sources are blocked"),
        (re.compile(r"\bresource\s+\"(?:local_file|local_sensitive_file)\""), "local file writes are blocked"),
        (re.compile(r"\bresource\s+\"aws_iam_(?:user|access_key|user_login_profile)\""), "IAM identity resources are blocked"),
        (re.compile(r"AKIA[0-9A-Z]{16}"), "hard-coded AWS access key id found"),
        (re.compile(r"ASIA[0-9A-Z]{16}"), "hard-coded temporary AWS key found"),
        (re.compile(r"aws_secret_access_key\s*="), "hard-coded AWS secret key found"),
        (re.compile(r"aws_access_key_id\s*="), "hard-coded AWS access key found"),
        (re.compile(r"\b(?:access_key|secret_key)\s*="), "hard-coded provider credentials found"),
        (re.compile(r"\b\w*password\s*=\s*\""), "hard-coded password found; use a variable"),
    ]

    for path in sorted(workdir.rglob("*")):
        if path.suffix not in {".tf", ".tfvars", ".json"}:
            continue
        if path.name.endswith(".tfstate") or path.name.endswith(".tfplan"):
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        rel = path.relative_to(workdir)
        for pattern, message in patterns:
            # Generic password checks only apply to HCL, not tfvars/json.
            if "password" in message and path.suffix != ".tf":
                continue
            if pattern.search(text):
                raise LiveError(f"{rel}: {message}")
        if path.suffix == ".tf" and re.search(r"map_public_ip_on_launch\s*=\s*true", text):
            warnings.append(f"{rel}: map_public_ip_on_launch = true (no instances in the pilot)")
    return warnings


def _open_cidr(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return value.strip() in {"0.0.0.0/0", "::/0"}
    if isinstance(value, (list, tuple, set)):
        return any(_open_cidr(item) for item in value)
    return False


def _private_cidr(value: Any) -> bool:
    try:
        return ipaddress.ip_network(str(value), strict=False).is_private
    except ValueError:
        return False


def _policy_is_public(policy: Any) -> bool:
    if not policy:
        return False
    if isinstance(policy, str):
        try:
            document = json.loads(policy)
        except json.JSONDecodeError:
            return True
    elif isinstance(policy, dict):
        document = policy
    else:
        return True

    statements = document.get("Statement", [])
    if isinstance(statements, dict):
        statements = [statements]
    for statement in statements:
        if not isinstance(statement, dict):
            continue
        if statement.get("Effect") != "Allow":
            continue
        principal = statement.get("Principal")
        if principal == "*":
            return True
        if isinstance(principal, dict):
            for value in principal.values():
                if value == "*":
                    return True
                if isinstance(value, list) and "*" in value:
                    return True
    return False


def _type_allowed(resource_type: str) -> bool:
    if resource_type in LIVE_ALLOWED_TYPES:
        return True
    if resource_type in LOCAL_TYPES:
        return True
    return any(resource_type.startswith(prefix) for prefix in LOCAL_PREFIXES)


def guard_plan(plan: dict[str, Any]) -> dict[str, Any]:
    """Inspect a Terraform plan JSON document before any apply.

    Only clean creates of allowlisted, low-cost resources are permitted.
    """
    changes = plan.get("resource_changes") or []
    managed: list[dict[str, Any]] = []
    for change in changes:
        if change.get("mode") != "managed":
            continue
        actions = (change.get("change") or {}).get("actions") or []
        if actions == ["no-op"]:
            continue
        managed.append(change)

    violations: list[str] = []
    warnings: list[str] = []
    types: set[str] = set()

    for change in managed:
        address = str(change.get("address", "?"))
        resource_type = str(change.get("type", ""))
        actions = (change.get("change") or {}).get("actions") or []
        after = (change.get("change") or {}).get("after") or {}
        types.add(resource_type)

        if actions != ["create"]:
            violations.append(
                f"{address}: action {actions} is not a clean create; destructive/update plans are blocked"
            )
            continue
        if not _type_allowed(resource_type):
            violations.append(
                f"{address}: resource type {resource_type} is not in the live allowlist"
            )
            continue

        if resource_type == "aws_vpc":
            cidr = after.get("cidr_block")
            if cidr and not _private_cidr(cidr):
                violations.append(f"{address}: VPC CIDR {cidr!r} is not private")
        elif resource_type == "aws_subnet":
            cidr = after.get("cidr_block")
            if cidr and not _private_cidr(cidr):
                violations.append(f"{address}: subnet CIDR {cidr!r} is not private")
            if after.get("map_public_ip_on_launch") is True:
                warnings.append(f"{address}: map_public_ip_on_launch = true")
        elif resource_type == "aws_security_group":
            for index, ingress in enumerate(after.get("ingress") or []):
                if not isinstance(ingress, dict):
                    continue
                if _open_cidr(ingress.get("cidr_blocks")) or _open_cidr(
                    ingress.get("ipv6_cidr_blocks")
                ):
                    violations.append(
                        f"{address}: ingress[{index}] allows 0.0.0.0/0 or ::/0"
                    )
        elif resource_type == "aws_security_group_rule":
            rule_type = after.get("type", "ingress")
            if rule_type == "ingress" and (
                _open_cidr(after.get("cidr_blocks"))
                or _open_cidr(after.get("ipv6_cidr_blocks"))
            ):
                violations.append(f"{address}: ingress allows 0.0.0.0/0 or ::/0")
        elif resource_type == "aws_s3_bucket":
            acl = after.get("acl")
            if acl and acl != "private":
                violations.append(f"{address}: bucket ACL {acl!r} is not private")
        elif resource_type == "aws_s3_bucket_acl":
            acl = after.get("acl")
            if acl and acl != "private":
                violations.append(f"{address}: bucket ACL {acl!r} is not private")
        elif resource_type == "aws_s3_bucket_public_access_block":
            for key in (
                "block_public_acls",
                "block_public_policy",
                "ignore_public_acls",
                "restrict_public_buckets",
            ):
                if after.get(key) is not True:
                    violations.append(f"{address}: {key} must be true")
        elif resource_type in {
            "aws_s3_bucket_policy",
            "aws_sqs_queue",
            "aws_sqs_queue_policy",
            "aws_sns_topic",
        }:
            if _policy_is_public(after.get("policy")):
                violations.append(f"{address}: policy allows a public principal")
        elif resource_type == "aws_dynamodb_table":
            if after.get("billing_mode") != "PAY_PER_REQUEST":
                violations.append(
                    f"{address}: DynamoDB must use PAY_PER_REQUEST billing in live mode"
                )
            if after.get("deletion_protection_enabled") is True:
                violations.append(f"{address}: DynamoDB deletion protection blocks cleanup")
        elif resource_type == "aws_route":
            if after.get("nat_gateway_id"):
                violations.append(f"{address}: NAT gateway routes are billable and blocked")
            if after.get("transit_gateway_id"):
                violations.append(f"{address}: Transit Gateway routes are billable and blocked")
        elif resource_type == "aws_cloudwatch_log_group":
            if after.get("retention_in_days") in (0, None):
                warnings.append(f"{address}: log group has no retention limit")

    if "aws_s3_bucket" in types and "aws_s3_bucket_public_access_block" not in types:
        violations.append(
            "S3 bucket created without aws_s3_bucket_public_access_block"
        )

    if violations:
        raise LiveError(
            "Live plan blocked before apply:\n- " + "\n- ".join(violations)
        )

    return {
        "resource_types": sorted(types),
        "resources": [str(change.get("address")) for change in managed],
        "warnings": warnings,
    }


def _var_args(overrides: dict[str, Any], user_var_file: Path | None) -> list[str]:
    args: list[str] = []
    if user_var_file:
        args.extend(["-var-file=arena.user.tfvars"])
    for name, value in overrides.items():
        args.extend(["-var", f"{name}={json.dumps(value)}"])
    return args


def _terraform(
    ctx: dict[str, Any],
    args: list[str],
    workdir: Path,
    timeout: int,
) -> dict[str, Any]:
    return _run([ctx["terraform"], *args], workdir, ctx["env"], timeout)


def _sweep(ctx: dict[str, Any], run_id: str) -> dict[str, Any]:
    """Look for leftovers by unique project tag and name prefixes.

    This is a best-effort safety net. Terraform destroy is the primary cleanup.
    """
    base = f"arena-{run_id}"
    checks: list[tuple[str, list[str]]] = [
        (
            "resourcegroupstaggingapi",
            [
                "resourcegroupstaggingapi",
                "get-resources",
                "--tag-filters",
                f"Key=Project,Values={base}",
                "--query",
                "ResourceTagMappingList[].ResourceARN",
            ],
        ),
        (
            "vpcs",
            [
                "ec2",
                "describe-vpcs",
                "--filters",
                f"Name=tag:Project,Values={base}",
                "--query",
                "Vpcs[].VpcId",
            ],
        ),
        (
            "sqs",
            [
                "sqs",
                "list-queues",
                "--queue-name-prefix",
                base,
                "--query",
                "QueueUrls[]",
            ],
        ),
        (
            "log-groups",
            [
                "logs",
                "describe-log-groups",
                "--log-group-name-prefix",
                f"/arena/{run_id}",
                "--query",
                "logGroups[].logGroupName",
            ],
        ),
        (
            "s3",
            [
                "s3api",
                "list-buckets",
                "--query",
                f"Buckets[?starts_with(Name, '{base}')].Name",
            ],
        ),
        (
            "dynamodb",
            [
                "dynamodb",
                "list-tables",
                "--query",
                f"TableNames[?starts_with(@, '{base}')]",
            ],
        ),
        (
            "sns",
            [
                "sns",
                "list-topics",
                "--query",
                f"Topics[?contains(TopicArn, '{base}')].TopicArn",
            ],
        ),
    ]

    residual: list[str] = []
    errors: list[dict[str, str]] = []
    for name, args in checks:
        result = _aws(ctx, args, timeout=60)
        if not result["ok"]:
            errors.append({"check": name, "error": (result.get("stderr") or "").strip()[:500]})
            continue
        try:
            items = json.loads(result["stdout"] or "[]")
        except json.JSONDecodeError:
            errors.append({"check": name, "error": "invalid JSON"})
            continue
        if not isinstance(items, list):
            items = [items]
        for item in items:
            if item and str(item) not in residual:
                residual.append(str(item))
    return {"residual": residual, "errors": errors}


def run_live(
    challenge: Challenge,
    *,
    profile: str | None = None,
    region: str | None = None,
    account: str | None = None,
    apply: bool = False,
    yes: bool = False,
    var_file: str | None = None,
    force: bool = False,
    keep: bool = False,
) -> dict[str, Any]:
    if apply and not yes:
        raise LiveError("Refusing to apply without --apply --yes.")
    if challenge.id not in PILOT_CHALLENGES:
        raise LiveError(
            f"Challenge {challenge.number:03d} ({challenge.id}) is not in the live "
            "pilot allowlist "
            f"({', '.join(sorted(PILOT_CHALLENGES))})."
        )

    ctx = preflight(profile, region, account, require_apply=apply)

    source = workspace_dir(challenge)
    files = read_workspace(source)
    if not files:
        raise LiveError(
            f"No .tf files in {source}. Run `python judge.py start {challenge.number}` "
            "and fill in the TODOs first."
        )
    static = evaluate(challenge, files)
    if apply and static["status"] != "PASS" and not force:
        raise LiveError(
            f"Static grading is {static['status']} ({static['score']}/100). "
            "Fix the failing tests, or pass --force to apply anyway."
        )

    run_id = new_run_id()
    overrides, missing, override_warnings = build_overrides(
        challenge, ctx["region"], run_id
    )
    if missing:
        raise LiveError(
            "These required variables need values; pass --var-file with a tfvars "
            f"file: {', '.join(missing)}"
        )

    candidate: Path | None = None
    if var_file:
        candidate = Path(var_file)
        if not candidate.exists():
            raise LiveError(f"Variable file not found: {candidate}")

    LIVE_TEMP.mkdir(parents=True, exist_ok=True)
    workdir = Path(
        tempfile.mkdtemp(prefix=f"arena-live-{challenge.number:03d}-", dir=str(LIVE_TEMP))
    )
    user_var_file: Path | None = workdir / "arena.user.tfvars" if candidate else None

    report: dict[str, Any] = {
        "ran": True,
        "mode": "apply" if apply else "plan",
        "challenge": {
            "number": challenge.number,
            "id": challenge.id,
            "title": challenge.title,
        },
        "account": ctx["account"],
        "arn": ctx["identity"].get("Arn"),
        "profile": ctx["profile"],
        "region": ctx["region"],
        "run_id": run_id,
        "overrides": _redact(overrides),
        "static": {
            "status": static["status"],
            "score": static["score"],
            "passed": static["passed"],
            "total": static["total"],
        },
        "init": None,
        "validate": None,
        "plan": None,
        "plan_guard": None,
        "apply": None,
        "outputs": None,
        "state": None,
        "destroy": None,
        "state_after_destroy": None,
        "sweep": None,
        "status": "FAIL",
        "error": None,
        "workdir": None,
        "duration_ms": 0,
    }
    started = time.monotonic()
    applied = False

    try:
        copy_workspace(challenge, workdir)
        if candidate and user_var_file:
            shutil.copy2(candidate, user_var_file)
        safety_warnings = check_workspace_safety(workdir)
        report["plan_guard"] = {"warnings": safety_warnings}

        for stale in workdir.glob("*.auto.tfvars*"):
            stale.unlink()
        (workdir / "arena.auto.tfvars.json").write_text(
            json.dumps(overrides, indent=2) + "\n", encoding="utf-8"
        )
        var_args = _var_args(overrides, user_var_file)

        init = _terraform(
            ctx, ["init", "-backend=false", "-input=false", "-no-color"], workdir, 300
        )
        report["init"] = _slim(init)
        if not init["ok"]:
            raise LiveError(
                "terraform init failed:\n"
                + (init.get("stderr") or init.get("stdout") or "")[-3000:]
            )

        validate = _terraform(ctx, ["validate", "-no-color"], workdir, 120)
        report["validate"] = _slim(validate)
        if not validate["ok"]:
            raise LiveError(
                "terraform validate failed:\n"
                + (validate.get("stderr") or validate.get("stdout") or "")[-3000:]
            )

        plan = _terraform(
            ctx,
            [
                "plan",
                "-input=false",
                "-no-color",
                "-out=arena.tfplan",
                *var_args,
            ],
            workdir,
            600,
        )
        report["plan"] = _slim(plan)
        if not plan["ok"]:
            raise LiveError(
                "terraform plan failed:\n"
                + (plan.get("stderr") or plan.get("stdout") or "")[-3000:]
            )

        show = _terraform(ctx, ["show", "-json", "arena.tfplan"], workdir, 120)
        if not show["ok"]:
            raise LiveError(
                "terraform show failed:\n"
                + (show.get("stderr") or show.get("stdout") or "")[-3000:]
            )
        plan_json = json.loads(show["stdout"] or "{}")
        guard = guard_plan(plan_json)
        guard["warnings"] = (
            report["plan_guard"].get("warnings", []) + guard.get("warnings", [])
        )
        report["plan_guard"] = guard

        if apply:
            applied = True
            applied_result = _terraform(
                ctx,
                [
                    "apply",
                    "-input=false",
                    "-no-color",
                    "-auto-approve",
                    "arena.tfplan",
                ],
                workdir,
                900,
            )
            report["apply"] = _slim(applied_result)
            if not applied_result["ok"]:
                raise LiveError(
                    "terraform apply failed:\n"
                    + (applied_result.get("stderr") or applied_result.get("stdout") or "")[
                        -3000:
                    ]
                )

            outputs = _terraform(ctx, ["output", "-json"], workdir, 60)
            if outputs["ok"]:
                try:
                    report["outputs"] = _redact_outputs(
                        json.loads(outputs["stdout"] or "{}")
                    )
                except json.JSONDecodeError:
                    report["outputs"] = {"error": "invalid output JSON"}
            else:
                report["outputs"] = {"error": (outputs.get("stderr") or "")[-1000:]}

            state = _terraform(ctx, ["state", "list"], workdir, 60)
            report["state"] = [
                line.strip()
                for line in (state.get("stdout") or "").splitlines()
                if line.strip()
            ]

        report["status"] = "PASS"
    except Exception as exc:
        report["status"] = "FAIL"
        report["error"] = f"{type(exc).__name__}: {exc}"
    finally:
        if applied:
            destroy = _terraform(
                ctx,
                ["destroy", "-input=false", "-no-color", "-auto-approve", *var_args],
                workdir,
                900,
            )
            report["destroy"] = _slim(destroy)
            state_after = _terraform(ctx, ["state", "list"], workdir, 60)
            report["state_after_destroy"] = [
                line.strip()
                for line in (state_after.get("stdout") or "").splitlines()
                if line.strip()
            ]
            sweep = _sweep(ctx, run_id)
            report["sweep"] = sweep
            if not destroy["ok"]:
                report["status"] = "FAIL"
                report["error"] = (
                    (report.get("error") or "")
                    + " | cleanup: terraform destroy failed"
                ).strip(" |")
            if report["state_after_destroy"]:
                report["status"] = "FAIL"
                report["error"] = (
                    (report.get("error") or "")
                    + " | cleanup: state is not empty after destroy"
                ).strip(" |")
            if sweep["residual"]:
                report["status"] = "FAIL"
                report["error"] = (
                    (report.get("error") or "")
                    + " | cleanup: residual resources found"
                ).strip(" |")

        cleanup_incomplete = (
            report["status"] != "PASS"
            and applied
            and (
                not (report.get("destroy") or {}).get("ok", False)
                or bool(report.get("state_after_destroy"))
                or bool((report.get("sweep") or {}).get("residual"))
            )
        )
        if keep or cleanup_incomplete:
            report["workdir"] = str(workdir)
        else:
            shutil.rmtree(workdir, ignore_errors=True)

        report["duration_ms"] = int((time.monotonic() - started) * 1000)

    return report


def print_report(report: dict[str, Any]) -> None:
    status = report.get("status", "FAIL")
    mode = report.get("mode", "plan")
    challenge = report.get("challenge") or {}
    print()
    print(f"[LIVE {status}] {challenge.get('number', '?'):>3}. {challenge.get('title', '?')}")
    print(
        f"Account: {report.get('account')} | Region: {report.get('region')} "
        f"| Profile: {report.get('profile')}"
    )
    print(
        f"Mode: {mode} | Run ID: {report.get('run_id')} "
        f"| Duration: {report.get('duration_ms', 0)} ms"
    )
    static = report.get("static") or {}
    print(
        f"Static: {static.get('status')} {static.get('score')}/100 "
        f"({static.get('passed')}/{static.get('total')})"
    )
    guard = report.get("plan_guard") or {}
    types = guard.get("resource_types") or []
    print(f"Plan: {', '.join(types) if types else 'no managed resources'}")
    for warning in guard.get("warnings") or []:
        print(f"  WARN {warning}")

    if mode == "apply":
        applied = report.get("apply") or {}
        destroy = report.get("destroy") or {}
        print(
            f"Apply: {'ok' if applied.get('ok') else 'not run/failed'} "
            f"({applied.get('duration_ms', 0)} ms)"
        )
        print(
            f"Destroy: {'ok' if destroy.get('ok') else 'FAILED'} "
            f"({destroy.get('duration_ms', 0)} ms)"
        )
        residual = (report.get("sweep") or {}).get("residual") or []
        print(f"Residual: {', '.join(residual) if residual else 'none'}")
        if report.get("state_after_destroy"):
            print(f"State after destroy: {', '.join(report['state_after_destroy'])}")
    else:
        print("No AWS resources applied (plan-only).")

    if report.get("error"):
        print()
        print(f"Error: {report['error']}")
    if report.get("workdir"):
        print(f"Kept for inspection: {report['workdir']}")
    print()
