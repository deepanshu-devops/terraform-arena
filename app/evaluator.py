"""Test-suite compiler: turns a submitted HCL bundle into a structured verdict."""
from __future__ import annotations

import re
import time
from dataclasses import dataclass, field
from typing import Callable, Optional

from . import checks as C
from .hcl import Config, norm, parse_files, unquote

CheckFn = Callable[[Config], tuple[bool, str]]


@dataclass
class TestCase:
    id: str
    title: str
    category: str
    weight: int
    fn: CheckFn
    required: bool = True
    hint: str = ""


@dataclass
class Challenge:
    id: str
    number: int
    title: str
    difficulty: str
    points: int
    tags: list[str]
    scenario: str
    constraints: list[str]
    variables: list[dict]
    expected_resources: list[str]
    expected_outputs: list[str]
    starter: dict[str, str]
    tests: list[TestCase]
    allowlist: list[str] = field(default_factory=list)
    data_allowlist: list[str] = field(default_factory=list)
    apply_sandbox: bool = False
    level: int = 0
    level_name: str = ""
    focus: dict = field(default_factory=dict)
    reference: dict = field(default_factory=dict)

    def public(self) -> dict:
        return {
            "id": self.id,
            "number": self.number,
            "title": self.title,
            "difficulty": self.difficulty,
            "points": self.points,
            "level": self.level,
            "level_name": self.level_name,
            "tags": self.tags,
            "scenario": self.scenario,
            "constraints": self.constraints,
            "variables": self.variables,
            "expected_resources": self.expected_resources,
            "expected_outputs": self.expected_outputs,
            "starter": self.starter,
            "focus": self.focus,
            "allowlist": self.allowlist,
            "apply_sandbox": self.apply_sandbox,
            "test_count": len(self.tests) + 1,
            # Hidden test details are NOT exposed until submission.
            "test_manifest": [
                {"id": t.id, "title": t.title, "category": t.category, "weight": t.weight}
                for t in self.tests
            ],
        }


# ---------------------------------------------------------------------------
# Security policy
# ---------------------------------------------------------------------------
GLOBAL_BLOCKED_TYPES = {
    # compute that can run away with a bill
    "aws_spot_fleet_request",
    "aws_ec2_fleet",
    "aws_batch_compute_environment",
    "aws_sagemaker_endpoint",
    "aws_sagemaker_notebook_instance",
    "aws_eks_cluster",
    "aws_eks_node_group",
    "aws_emr_cluster",
    "aws_redshift_cluster",
    "aws_rds_cluster",
    "aws_rds_global_cluster",
    "aws_neptune_cluster",
    "aws_docdb_cluster",
    "aws_elasticache_cluster",
    "aws_elasticache_replication_group",
    "aws_opensearch_domain",
    "aws_elasticsearch_domain",
    "aws_kinesis_stream",
    "aws_msk_cluster",
    "aws_glue_job",
    "aws_lambda_function_url",
    # identity / account level
    "aws_iam_user",
    "aws_iam_access_key",
    "aws_iam_user_policy",
    "aws_iam_user_policy_attachment",
    "aws_organizations_account",
    "aws_organizations_organization",
    "aws_account_alternate_contact",
    "aws_guardduty_detector",
    "aws_config_configuration_recorder",
    "aws_cloudtrail",
}

GLOBAL_SUPPORT_TYPES = {
    "random_id",
    "random_string",
    "random_pet",
    "random_uuid",
    "aws_kms_key",
    "aws_kms_alias",
    "aws_caller_identity",
    "aws_region",
    "terraform_data",
    "null_resource",
    "local_file",
}

SMALL_INSTANCE_TYPES = {"t2.micro", "t2.small", "t3.micro", "t3.small", "t4g.micro", "t4g.small"}

BLOCKED_PROVIDERS = {"google", "azurerm", "alicloud", "oci", "ibm", "vcd"}

ALLOWED_PROVIDERS = {"aws", "docker", "random", "archive", "local", "null", "terraform"}


def security_scan(challenge: Challenge, cfg: Config) -> dict:
    blocked: list[str] = []
    warnings: list[str] = []

    # providers
    declared = set(cfg.required_providers().keys()) | set(cfg.providers().keys())
    for p in declared:
        if p in BLOCKED_PROVIDERS:
            blocked.append(f"Provider '{p}' is not allowed on this platform.")
        elif p not in ALLOWED_PROVIDERS:
            warnings.append(f"Provider '{p}' is not on the allowlist.")

    allow = set(challenge.allowlist) | GLOBAL_SUPPORT_TYPES

    # resource types
    for res in cfg.resources():
        rtype = res.labels[0] if res.labels else "unknown"
        if rtype in GLOBAL_BLOCKED_TYPES:
            blocked.append(f"Resource type '{rtype}' is blocked by platform policy.")
        elif challenge.allowlist and rtype not in allow:
            blocked.append(
                f"Resource type '{rtype}' is outside this challenge's allowlist."
            )

    # data sources
    for ds in cfg.data_sources():
        dtype = ds.labels[0] if ds.labels else "unknown"
        if dtype == "external":
            blocked.append("data 'external' is blocked (arbitrary command execution).")
        elif challenge.data_allowlist and dtype not in challenge.data_allowlist:
            warnings.append(f"Data source 'data.{dtype}' is not on the allowlist.")

    # provisioners / shell execution
    for res in cfg.resources():
        for prov in res.nested("provisioner"):
            name = prov.labels[0] if prov.labels else "?"
            if name in ("local-exec", "remote-exec"):
                blocked.append(
                    f"Provisioner '{name}' on {res.labels[0]} is blocked (shell execution)."
                )

    # expensive instance sizes
    for res in cfg.resources():
        it = C.raw(res, "instance_type")
        if it:
            kind, val = C.value(res, "instance_type")
            if kind == "string" and val not in SMALL_INSTANCE_TYPES:
                blocked.append(
                    f"instance_type '{val}' is not on the free-tier allowlist "
                    f"({', '.join(sorted(SMALL_INSTANCE_TYPES))})."
                )

    # wildcard IAM actions
    for fname, src in cfg.files.items():
        if re.search(r'Action\s*=\s*(\[?\s*"\*"|"\*")', src):
            blocked.append(f"{fname}: wildcard IAM Action '*' is blocked (least privilege).")

    # runaway loops
    for res in cfg.resources():
        for loop_attr in ("count", "for_each"):
            r = C.raw(res, loop_attr)
            if r and re.fullmatch(r"\d+", norm(r)) and int(norm(r)) > 20:
                blocked.append(
                    f"{res.labels[0]}: {loop_attr}={r} exceeds the max resource cap (20)."
                )

    # resource count cap
    if len(cfg.resources()) > 60:
        blocked.append(f"Submission creates {len(cfg.resources())} resources (cap: 60).")

    # credentials
    cred_ok, cred_detail = C.no_hardcoded_credentials(cfg)
    if not cred_ok:
        blocked.append(cred_detail)

    return {"blocked": blocked, "warnings": warnings}


# ---------------------------------------------------------------------------
# Formatting / variable / drift graders
# ---------------------------------------------------------------------------
def grade_formatting(files: dict[str, str]) -> dict:
    issues = C.formatting_issues(files)
    score = max(0, 100 - 5 * len(issues))
    return {
        "score": score,
        "grade": C.grade_from_score(score),
        "issues": issues,
    }


def grade_variables(challenge: Challenge, cfg: Config) -> dict:
    checks: list[dict] = []
    used = cfg.referenced_variables()
    for spec in challenge.variables:
        name = spec["name"]
        var = C.get_var(cfg, name)
        entry = {"name": name, "issues": []}
        if not var:
            entry["issues"].append("not defined")
            checks.append(entry)
            continue
        expected_type = spec.get("type")
        if expected_type and norm(C.var_type(var) or "") != norm(expected_type):
            entry["issues"].append(
                f"type is {C.var_type(var)!r}, expected {expected_type!r}"
            )
        if "default" in spec and spec["default"] is not None:
            _, got = C.var_default(var)
            if got != spec["default"]:
                entry["issues"].append(
                    f"default is {got!r}, expected {spec['default']!r}"
                )
        if spec.get("validation") and not var.nested("validation"):
            entry["issues"].append("missing validation block")
        if spec.get("used", True) and name not in used:
            entry["issues"].append("declared but never referenced")
        checks.append(entry)

    total = len(checks) or 1
    passed = sum(1 for c in checks if not c["issues"])
    score = round(100 * passed / total)
    return {
        "score": score,
        "grade": C.grade_from_score(score),
        "checks": checks,
    }


def detect_drift(challenge: Challenge, cfg: Config) -> list[dict]:
    drift: list[dict] = []
    found_types = {r.labels[0] for r in cfg.resources() if r.labels}
    allow = set(challenge.allowlist) | GLOBAL_SUPPORT_TYPES

    for rtype in challenge.expected_resources:
        if rtype not in found_types:
            drift.append(
                {
                    "severity": "error",
                    "message": f"Missing expected resource: {rtype}",
                }
            )

    for rtype in sorted(found_types):
        if challenge.allowlist and rtype not in allow:
            drift.append(
                {
                    "severity": "warning",
                    "message": f"Unexpected resource outside the challenge scope: {rtype}",
                }
            )

    # hardcoded provider region
    aws_provider = cfg.providers().get("aws")
    if aws_provider:
        region = C.raw(aws_provider, "region")
        if region and unquote(region) is not None:
            drift.append(
                {
                    "severity": "warning",
                    "message": f"AWS region is hardcoded ({region}); parameterize with var.aws_region.",
                }
            )

    # declared-but-unused variables
    declared = set(cfg.variables())
    used = cfg.referenced_variables()
    for name in sorted(declared - used):
        drift.append(
            {
                "severity": "info",
                "message": f"Variable '{name}' is declared but never used.",
            }
        )

    # outputs referencing missing resources is not checked statically
    return drift


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------
def evaluate(challenge: Challenge, files: dict[str, str]) -> dict:
    started = time.perf_counter()
    cfg = parse_files(files)

    tests: list[dict] = []

    # Syntax gate
    syntax_ok = len(cfg.errors) == 0
    syntax_detail = (
        "HCL parsed successfully."
        if syntax_ok
        else "; ".join(
            f"{e['file']}:{e['line']}: {e['message']}" for e in cfg.errors[:8]
        )
    )
    tests.append(
        {
            "id": "syntax",
            "title": "HCL syntax & brace balance",
            "category": "Syntax",
            "weight": 10,
            "required": True,
            "passed": syntax_ok,
            "detail": syntax_detail,
        }
    )

    # Challenge tests
    for tc in challenge.tests:
        try:
            passed, detail = tc.fn(cfg)
        except Exception as exc:  # pragma: no cover - defensive
            passed, detail = False, f"Internal check error: {exc}"
        tests.append(
            {
                "id": tc.id,
                "title": tc.title,
                "category": tc.category,
                "weight": tc.weight,
                "required": tc.required,
                "passed": bool(passed),
                "detail": detail,
            }
        )

    security = security_scan(challenge, cfg)

    total_weight = sum(t["weight"] for t in tests) or 1
    passed_weight = sum(t["weight"] for t in tests if t["passed"])
    score = round(100 * passed_weight / total_weight)

    required_failed = [t for t in tests if t["required"] and not t["passed"]]
    status = (
        "PASS"
        if not required_failed and not security["blocked"] and syntax_ok
        else "FAIL"
    )

    categories: dict[str, dict] = {}
    for t in tests:
        cat = categories.setdefault(
            t["category"], {"passed": 0, "total": 0, "weight": 0}
        )
        cat["total"] += 1
        cat["weight"] += t["weight"]
        if t["passed"]:
            cat["passed"] += 1

    formatting = grade_formatting(files)
    variables = grade_variables(challenge, cfg)
    drift = detect_drift(challenge, cfg)

    duration_ms = round((time.perf_counter() - started) * 1000, 2)

    return {
        "status": status,
        "score": score,
        "passed": sum(1 for t in tests if t["passed"]),
        "total": len(tests),
        "duration_ms": duration_ms,
        "challenge_id": challenge.id,
        "challenge_title": challenge.title,
        "tests": tests,
        "categories": categories,
        "security": security,
        "formatting": formatting,
        "variables": variables,
        "drift": drift,
        "syntax_errors": cfg.errors,
        "resource_types": cfg.all_resource_types(),
    }
