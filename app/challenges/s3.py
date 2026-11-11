"""Challenge 01 — Secure S3 Bucket Provisioning (Easy)."""
from __future__ import annotations

import re

from .. import checks as C
from ..evaluator import Challenge, TestCase
from ..hcl import has_ref, norm


def _patterns(text: str) -> list[str]:
    return re.findall(r'"([^"]*)"', text or "")


def t_provider(cfg):
    ok, msg = C.required_provider(cfg, "aws")
    if not ok:
        return False, msg
    if "aws" not in cfg.providers():
        return False, 'Missing provider "aws" configuration block.'
    return True, "AWS provider is declared and configured."


def t_region_var(cfg):
    provider = cfg.providers().get("aws")
    if not provider:
        return False, 'Missing provider "aws" block.'
    return C.is_ref(provider, "region", "var.aws_region")


def t_bucket_var(cfg):
    return C.variable_defined(
        cfg, "bucket_name", expected_type="string", require_validation=True
    )


def t_bucket_validation(cfg):
    var = C.get_var(cfg, "bucket_name")
    if not var:
        return False, "Variable 'bucket_name' is not defined."
    text = C.validation_text(var)
    if not text:
        return False, "bucket_name has no validation condition."
    pats = _patterns(text)
    charset = any(("a-z" in p and "0-9" in p and "-" in p) for p in pats)
    length = ("length(" in text) or any(
        "{3,63}" in p.replace(" ", "") or "{3, 63}" in p for p in pats
    )
    refs = has_ref(text, "var.bucket_name")
    if charset and length and refs:
        return True, "bucket_name validation enforces charset and 3–63 length."
    missing = []
    if not charset:
        missing.append("lowercase/hyphen charset regex")
    if not length:
        missing.append("3–63 length rule")
    if not refs:
        missing.append("reference to var.bucket_name")
    return False, "Validation is missing: " + ", ".join(missing) + "."


def t_env_var(cfg):
    var = C.get_var(cfg, "environment")
    if not var:
        return False, "Variable 'environment' is not defined."
    if norm(C.var_type(var) or "") != "string":
        return False, f"environment must be type string, found {C.var_type(var)!r}."
    text = C.validation_text(var)
    if not text:
        return False, "environment has no validation condition."
    pats = " ".join(_patterns(text))
    has_contains = "contains(" in text
    has_values = all(v in pats for v in ("dev", "staging", "prod"))
    if has_contains and has_values:
        return True, "environment is restricted to dev/staging/prod."
    return False, "environment validation must use contains([...]) with dev, staging and prod."


def t_region_default(cfg):
    return C.variable_defined(
        cfg, "aws_region", expected_type="string", expected_default="us-east-1"
    )


def t_versioning_default(cfg):
    var = C.get_var(cfg, "enable_versioning")
    if not var:
        return False, "Variable 'enable_versioning' is not defined."
    if norm(C.var_type(var) or "") != "bool":
        return False, f"enable_versioning must be bool, found {C.var_type(var)!r}."
    _, default = C.var_default(var)
    if default is not True:
        return False, f"enable_versioning default must be true, found {default!r}."
    return True, "enable_versioning is a bool defaulting to true."


def t_project_default(cfg):
    return C.variable_defined(
        cfg,
        "project_name",
        expected_type="string",
        expected_default="terraform-practice",
    )


def t_bucket_resource(cfg):
    bucket = C.first_resource(cfg, "aws_s3_bucket")
    if not bucket:
        return False, "Missing aws_s3_bucket resource."
    name = C.raw(bucket, "bucket")
    if not name:
        return False, "aws_s3_bucket is missing the 'bucket' argument."
    if not has_ref(name, "var.bucket_name"):
        return False, f"Bucket name must come from var.bucket_name, found {name!r}."
    return True, "Bucket name is parameterized from var.bucket_name."


def t_no_deprecated(cfg):
    bucket = C.first_resource(cfg, "aws_s3_bucket")
    if not bucket:
        return False, "Missing aws_s3_bucket resource."
    found = []
    for attr in ("versioning", "server_side_encryption_configuration", "acl"):
        if bucket.attr(attr):
            found.append(attr)
    for block in ("versioning", "server_side_encryption_configuration", "logging", "cors_rule"):
        if bucket.nested(block):
            found.append(block + " {}")
    if found:
        return False, "Deprecated inline argument(s) on aws_s3_bucket: " + ", ".join(found)
    return True, "No deprecated inline S3 arguments detected."


def t_versioning_resource(cfg):
    resource = C.first_resource(cfg, "aws_s3_bucket_versioning")
    if not resource:
        return False, "Missing aws_s3_bucket_versioning resource."
    if not resource.nested("versioning_configuration"):
        return False, "aws_s3_bucket_versioning is missing versioning_configuration."
    status = C.raw(resource.nested("versioning_configuration")[0], "status")
    if status is None:
        return False, "versioning_configuration.status is missing."
    if "Enabled" in status:
        return True, f"Versioning status resolves to Enabled ({status})."
    return False, f"Versioning status must be Enabled, found {status!r}."


def t_encryption(cfg):
    resource = C.first_resource(cfg, "aws_s3_bucket_server_side_encryption_configuration")
    if not resource:
        return False, "Missing server-side encryption configuration resource."
    rules = resource.nested("rule")
    if not rules:
        return False, "Encryption configuration is missing a 'rule' block."
    applies = rules[0].nested("apply_server_side_encryption_by_default")
    if not applies:
        return False, "Missing apply_server_side_encryption_by_default block."
    sse = C.raw(applies[0], "sse_algorithm")
    if sse is None:
        return False, "sse_algorithm is missing."
    if "AES256" not in sse:
        return False, f"Expected sse_algorithm AES256, found {sse!r}."
    return True, "SSE is enabled with AES256."


def t_public_access(cfg):
    resource = C.first_resource(cfg, "aws_s3_bucket_public_access_block")
    if not resource:
        return False, "Missing aws_s3_bucket_public_access_block resource."
    missing = []
    for attr in (
        "block_public_acls",
        "block_public_policy",
        "ignore_public_acls",
        "restrict_public_buckets",
    ):
        ok, _ = C.is_true(resource, attr)
        if not ok:
            missing.append(attr)
    if missing:
        return False, "Public access flags must all be true: " + ", ".join(missing)
    return True, "All four public access block flags are true."


def t_bucket_tags(cfg):
    issues = []
    for key, expected in (
        ("Project", "var.project_name"),
        ("Environment", "var.environment"),
        ("ManagedBy", '"terraform"'),
    ):
        ok, msg = C.tag_value(cfg, "aws_s3_bucket", key)
        if not ok:
            issues.append(msg)
        else:
            merged = C.effective_tags(cfg, C.first_resource(cfg, "aws_s3_bucket"))
            if norm(merged.get(key, "")) != norm(expected):
                issues.append(f"tag '{key}' expected {expected!r}, found {merged.get(key)!r}")
    if issues:
        return False, "; ".join(issues)
    return True, "Bucket carries Project, Environment and ManagedBy tags."


def t_outputs(cfg):
    missing = []
    for name in ("bucket_id", "bucket_arn", "bucket_region"):
        ok, msg = C.output_ok(cfg, name)
        if not ok:
            missing.append(msg)
    if missing:
        return False, "; ".join(missing)
    return True, "bucket_id, bucket_arn and bucket_region outputs exist."


def t_no_public_acl(cfg):
    return C.no_public_acl(cfg)


def t_var_usage(cfg):
    used = cfg.referenced_variables()
    missing = [
        n
        for n in ("bucket_name", "environment", "aws_region", "project_name")
        if n not in used
    ]
    if missing:
        return False, "Variables declared but not referenced: " + ", ".join(missing)
    return True, "Core variables are wired into resources."


CHALLENGE = Challenge(
    id="secure-s3-bucket",
    number=1,
    title="Secure S3 Bucket Provisioning",
    difficulty="Easy",
    points=100,
    tags=["aws", "s3", "security", "variables"],
    scenario=(
        "A new application team needs a storage bucket. Provision an AWS S3 bucket that is "
        "secure-by-default: versioning enabled, server-side encryption at rest using AES-256, "
        "and all forms of public access blocked. The configuration must be reusable across "
        "dev / staging / prod environments without editing resource blocks, and it must never "
        "hardcode credentials."
    ),
    constraints=[
        "Provider: AWS (hashicorp/aws); region parameterized via var.aws_region (default us-east-1).",
        "No hardcoded AWS credentials anywhere in the configuration.",
        "bucket_name must be a variable with validation: lowercase alphanumerics + hyphens, length 3–63.",
        "environment must be a variable restricted to dev, staging or prod.",
        "The S3 bucket must carry tags: Project, Environment, ManagedBy = \"terraform\".",
        "Use the modern split-resource style; no deprecated inline arguments on aws_s3_bucket.",
        "All four public access block flags must be true.",
        "Outputs must expose bucket_id, bucket_arn and bucket_region.",
        "Code must pass terraform fmt conventions (2-space indents, trailing newline, no tabs).",
    ],
    variables=[
        {"name": "bucket_name", "type": "string", "default": None, "validation": True},
        {"name": "environment", "type": "string", "default": "dev", "validation": True},
        {"name": "aws_region", "type": "string", "default": "us-east-1"},
        {"name": "enable_versioning", "type": "bool", "default": True},
        {"name": "project_name", "type": "string", "default": "terraform-practice"},
    ],
    expected_resources=[
        "aws_s3_bucket",
        "aws_s3_bucket_versioning",
        "aws_s3_bucket_server_side_encryption_configuration",
        "aws_s3_bucket_public_access_block",
    ],
    expected_outputs=["bucket_id", "bucket_arn", "bucket_region"],
    starter={
        "versions.tf": (
            "# versions.tf\n"
            "# TODO: declare required_version and the AWS provider (source + version).\n"
        ),
        "variables.tf": (
            "# variables.tf\n"
            "# TODO: declare bucket_name, environment, aws_region, enable_versioning, project_name.\n"
        ),
        "main.tf": (
            "# main.tf\n"
            "# TODO: configure the AWS provider and create the S3 resources.\n"
        ),
        "outputs.tf": (
            "# outputs.tf\n"
            "# TODO: expose bucket_id, bucket_arn and bucket_region.\n"
        ),
    },
    allowlist=[
        "aws_s3_bucket",
        "aws_s3_bucket_versioning",
        "aws_s3_bucket_server_side_encryption_configuration",
        "aws_s3_bucket_public_access_block",
        "aws_s3_bucket_ownership_controls",
    ],
    data_allowlist=["aws_region", "aws_caller_identity"],
    tests=[
        TestCase("s3-provider", "AWS provider + required_providers", "Providers", 6, t_provider),
        TestCase("s3-region-var", "Region parameterized via var.aws_region", "Providers", 6, t_region_var),
        TestCase("s3-var-bucket", "bucket_name variable typed + validated", "Variables", 6, t_bucket_var),
        TestCase("s3-validation", "bucket_name charset & length validation", "Variables", 8, t_bucket_validation),
        TestCase("s3-env-var", "environment restricted to dev/staging/prod", "Variables", 7, t_env_var),
        TestCase("s3-region-default", "aws_region default us-east-1", "Variables", 4, t_region_default),
        TestCase("s3-versioning-default", "enable_versioning bool default true", "Variables", 4, t_versioning_default),
        TestCase("s3-project-default", "project_name default terraform-practice", "Variables", 4, t_project_default),
        TestCase("s3-bucket", "Bucket name references var.bucket_name", "Resources", 7, t_bucket_resource),
        TestCase("s3-no-deprecated", "No deprecated inline S3 arguments", "Lifecycle", 7, t_no_deprecated),
        TestCase("s3-versioning", "Versioning enabled via split resource", "Lifecycle", 7, t_versioning_resource),
        TestCase("s3-encryption", "AES256 server-side encryption", "Security", 7, t_encryption),
        TestCase("s3-public-access", "All public access blocked", "Security", 8, t_public_access),
        TestCase("s3-tags", "Consistent bucket tags", "Lifecycle", 5, t_bucket_tags),
        TestCase("s3-outputs", "Required outputs exposed", "Outputs", 5, t_outputs),
        TestCase("s3-acl", "No public ACL", "Security", 4, t_no_public_acl),
        TestCase("s3-usage", "Variables wired into resources", "Modularity", 5, t_var_usage),
    ],
)
