"""Reference-solution generation and focused starter masking.

Every challenge is authored as a complete, working configuration.  The learner
gets that whole configuration with exactly one graded region replaced by a
``TODO`` comment.  This mirrors the LeetCode model: the surrounding program is
provided, and only the function body (here, an HCL block or attribute) is the
exercise.

The generator below synthesises a complete reference from a declarative spec.
It is intentionally test-driven: the spec's checks tell us which attributes,
nested blocks, outputs and textual constructs the reference must contain.  A
small table of Terraform defaults fills in required arguments that the tests do
not mention, so the reference also looks like a plausible real configuration.

Focus markers are comments emitted only in the reference.  ``mask_reference``
turns the marked region into a single TODO comment for the starter.
"""
from __future__ import annotations

import re
from collections import OrderedDict
from dataclasses import dataclass, field
from typing import Any, Iterable

FOCUS_START = "# arena:focus-start"
FOCUS_END = "# arena:focus-end"

LEVEL_NAMES = {
    0: "Level 0 - HCL Foundations",
    1: "Level 1 - Terraform Language",
    2: "Level 2 - First Resources",
    3: "Level 3 - Real Infrastructure",
    4: "Level 4 - Composition",
    5: "Level 5 - Modules & Capstones",
}


# ---------------------------------------------------------------------------
# Small HCL tree
# ---------------------------------------------------------------------------
class Node:
    """An HCL body: ordered attributes plus repeatable nested blocks."""

    __slots__ = ("attrs", "blocks")

    def __init__(self) -> None:
        self.attrs: OrderedDict[str, str] = OrderedDict()
        self.blocks: OrderedDict[str, list[Node]] = OrderedDict()

    def set(self, name: str, value: str) -> None:
        self.attrs[name] = value

    def setdefault(self, name: str, value: str) -> None:
        self.attrs.setdefault(name, value)

    def has(self, name: str) -> bool:
        return name in self.attrs

    def child(self, name: str) -> Node:
        nodes = self.blocks.setdefault(name, [])
        if not nodes:
            nodes.append(Node())
        return nodes[0]

    def add(self, name: str) -> Node:
        node = Node()
        self.blocks.setdefault(name, []).append(node)
        return node

    def path(self, *names: str) -> Node:
        node = self
        for name in names:
            node = node.child(name)
        return node


@dataclass
class Res:
    """A resource or data-source block under construction."""

    rtype: str
    name: str = "this"
    kind: str = "resource"  # resource | data
    root: Node = field(default_factory=Node)

    def attr(self, name: str, value: str) -> None:
        self.root.set(name, value)

    def ensure(self, name: str, value: str) -> None:
        self.root.setdefault(name, value)

    def block(self, name: str) -> Node:
        return self.root.child(name)

    def add_block(self, name: str) -> Node:
        return self.root.add(name)


@dataclass
class Focus:
    kind: str
    file: str = "main.tf"
    rtype: str = ""
    name: str = "this"
    path: tuple[str, ...] = ()
    attr: str = ""
    block: str = ""
    var: str = ""
    output: str = ""
    title: str = ""
    todo: str = ""

    def public(self) -> dict:
        return {
            "file": self.file,
            "kind": self.kind,
            "title": self.title or "Complete the graded block",
            "todo": self.todo or "Complete this block.",
        }


# ---------------------------------------------------------------------------
# Terraform defaults (required args not covered by the tests)
# ---------------------------------------------------------------------------
def _d(rtype: str, *pairs: tuple[str, str]) -> tuple[str, list[tuple[str, str]]]:
    return rtype, list(pairs)


RESOURCE_DEFAULTS: dict[str, list[tuple[str, str]]] = dict(
    [
        _d("aws_s3_bucket", ("bucket", '"app-assets"')),
        _d("aws_s3_bucket_versioning", ("bucket", "var.bucket_name")),
        _d("aws_s3_bucket_public_access_block", ("bucket", "var.bucket_name")),
        _d(
            "aws_s3_bucket_server_side_encryption_configuration",
            ("bucket", "var.bucket_name"),
        ),
        _d("aws_s3_bucket_lifecycle_configuration", ("bucket", "var.bucket_name")),
        _d("aws_s3_bucket_policy", ("bucket", "var.bucket_name")),
        _d("aws_kms_key", ("description", '"Arena managed key"')),
        _d(
            "aws_kms_alias",
            ("name", '"alias/arena-key"'),
            ("target_key_id", "aws_kms_key.this.id"),
        ),
        _d(
            "aws_instance",
            ("ami", '"ami-0123456789abcdef0"'),
            ("instance_type", '"t3.micro"'),
        ),
        _d(
            "aws_security_group",
            ("name", '"app-sg"'),
            ("description", '"Application security group"'),
        ),
        _d(
            "aws_security_group_rule",
            ("type", '"ingress"'),
            ("from_port", "443"),
            ("to_port", "443"),
            ("protocol", '"tcp"'),
            ("cidr_blocks", '["0.0.0.0/0"]'),
        ),
        _d("aws_vpc", ("cidr_block", '"10.0.0.0/16"')),
        _d("aws_subnet", ("cidr_block", '"10.0.1.0/24"')),
        _d("aws_internet_gateway"),
        _d("aws_route_table"),
        _d("aws_route", ("destination_cidr_block", '"0.0.0.0/0"')),
        _d("aws_route_table_association"),
        _d("aws_nat_gateway", ("allocation_id", "aws_eip.this.id")),
        _d("aws_eip", ("domain", '"vpc"')),
        _d("aws_eip_association", ("instance_id", "aws_instance.this.id")),
        _d(
            "aws_lb",
            ("name", '"app-alb"'),
            ("load_balancer_type", '"application"'),
        ),
        _d(
            "aws_lb_target_group",
            ("name", '"app-tg"'),
            ("port", "80"),
            ("protocol", '"HTTP"'),
        ),
        _d("aws_lb_listener", ("port", "80"), ("protocol", '"HTTP"')),
        _d(
            "aws_lb_target_group_attachment",
            ("target_id", "aws_instance.this.id"),
            ("port", "80"),
        ),
        _d(
            "aws_autoscaling_group",
            ("name", '"app-asg"'),
            ("min_size", "1"),
            ("max_size", "2"),
            ("desired_capacity", "1"),
        ),
        _d(
            "aws_launch_template",
            ("name", '"app-lt"'),
            ("image_id", '"ami-0123456789abcdef0"'),
            ("instance_type", '"t3.micro"'),
        ),
        _d(
            "aws_db_instance",
            ("identifier", '"app-db"'),
            ("engine", '"postgres"'),
            ("engine_version", '"15"'),
            ("instance_class", '"db.t3.micro"'),
            ("allocated_storage", "20"),
            ("skip_final_snapshot", "true"),
        ),
        _d("aws_db_subnet_group", ("name", '"app-db-subnets"')),
        _d(
            "aws_dynamodb_table",
            ("name", '"app-table"'),
            ("billing_mode", '"PAY_PER_REQUEST"'),
            ("hash_key", '"id"'),
        ),
        _d(
            "aws_lambda_function",
            ("function_name", '"app-fn"'),
            ("runtime", '"python3.12"'),
            ("handler", '"index.handler"'),
            ("filename", '"lambda.zip"'),
            ("memory_size", "128"),
        ),
        _d(
            "aws_lambda_permission",
            ("statement_id", '"allow-apigw"'),
            ("action", '"lambda:InvokeFunction"'),
        ),
        _d("aws_iam_role", ("name", '"app-role"')),
        _d("aws_iam_policy", ("name", '"app-policy"')),
        _d(
            "aws_iam_role_policy_attachment",
            ("role", "aws_iam_role.this.name"),
            ("policy_arn", "aws_iam_policy.this.arn"),
        ),
        _d(
            "aws_iam_role_policy",
            ("role", "aws_iam_role.this.id"),
            ("policy", 'jsonencode({ Version = "2012-10-17", Statement = [] })'),
        ),
        _d(
            "aws_cloudwatch_log_group",
            ("name", '"/aws/app"'),
            ("retention_in_days", "14"),
        ),
        _d(
            "aws_cloudwatch_metric_alarm",
            ("alarm_name", '"app-alarm"'),
            ("comparison_operator", '"GreaterThanThreshold"'),
            ("evaluation_periods", "1"),
            ("metric_name", '"CPUUtilization"'),
            ("namespace", '"AWS/EC2"'),
            ("period", "300"),
            ("statistic", '"Average"'),
            ("threshold", "80"),
        ),
        _d(
            "aws_cloudwatch_event_rule",
            ("name", '"app-rule"'),
            ("schedule_expression", '"rate(5 minutes)"'),
        ),
        _d("aws_cloudwatch_event_target", ("rule", "aws_cloudwatch_event_rule.this.name")),
        _d("aws_sns_topic", ("name", '"app-topic"')),
        _d("aws_sns_topic_subscription", ("protocol", '"sqs"')),
        _d("aws_sqs_queue", ("name", '"app-queue"')),
        _d("aws_cloudfront_distribution", ("enabled", "true")),
        _d("aws_acm_certificate", ("domain_name", '"example.com"')),
        _d(
            "aws_route53_record",
            ("name", '"www.example.com"'),
            ("type", '"A"'),
        ),
        _d("aws_route53_zone", ("name", '"example.com"')),
        _d("aws_ecs_cluster", ("name", '"app-cluster"')),
        _d(
            "aws_ecs_task_definition",
            ("family", '"app-task"'),
            ("cpu", "256"),
            ("memory", "512"),
            ("network_mode", '"awsvpc"'),
            ("requires_compatibilities", '["FARGATE"]'),
        ),
        _d(
            "aws_ecs_service",
            ("name", '"app-service"'),
            ("desired_count", "1"),
            ("launch_type", '"FARGATE"'),
        ),
        _d("aws_efs_file_system", ("creation_token", '"app-efs"')),
        _d("aws_efs_mount_target"),
        _d("aws_flow_log", ("traffic_type", '"ALL"')),
        _d("aws_backup_vault", ("name", '"app-vault"')),
        _d("aws_backup_plan", ("name", '"app-plan"')),
        _d("aws_secretsmanager_secret", ("name", '"app-secret"')),
        _d(
            "aws_secretsmanager_secret_version",
            ("secret_id", "aws_secretsmanager_secret.this.id"),
            ("secret_string", '"change-me"'),
        ),
        _d("aws_cognito_user_pool", ("name", '"app-users"')),
        _d(
            "aws_apigatewayv2_api",
            ("name", '"app-api"'),
            ("protocol_type", '"HTTP"'),
        ),
        _d(
            "aws_apigatewayv2_integration",
            ("integration_type", '"AWS_PROXY"'),
            ("payload_format_version", '"2.0"'),
        ),
        _d("aws_apigatewayv2_route", ("route_key", '"GET /items"')),
        _d(
            "aws_apigatewayv2_stage",
            ("name", '"$default"'),
            ("auto_deploy", "true"),
        ),
        _d("aws_ecr_repository", ("name", '"app-repo"')),
        _d(
            "aws_ebs_volume",
            ("availability_zone", '"us-east-1a"'),
            ("size", "20"),
        ),
        _d(
            "aws_key_pair",
            ("key_name", '"app-key"'),
            ("public_key", '"ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC7"'),
        ),
        _d(
            "aws_ssm_parameter",
            ("name", '"/app/config"'),
            ("type", '"String"'),
            ("value", '"example"'),
        ),
        _d(
            "aws_stepfunctions_state_machine",
            ("name", '"app-state-machine"'),
            (
                "definition",
                'jsonencode({ StartAt = "Done", States = { Done = { Type = "Succeed" } } })',
            ),
            ("role_arn", "aws_iam_role.this.arn"),
        ),
        _d("aws_wafv2_web_acl", ("name", '"app-waf"'), ("scope", '"REGIONAL"')),
        _d("docker_image"),
        _d("docker_container"),
        _d("docker_network"),
        _d("docker_volume"),
    ]
)

# Required nested blocks that are not necessarily asserted by tests.
NESTED_DEFAULTS: dict[str, list[tuple[tuple[str, ...], str, str]]] = {
    "aws_s3_bucket_versioning": [(("versioning_configuration",), "status", '"Enabled"')],
    "aws_s3_bucket_lifecycle_configuration": [
        (("rule",), "status", '"Enabled"'),
        (("rule", "expiration"), "days", "30"),
    ],
    "aws_s3_bucket_server_side_encryption_configuration": [
        (("rule", "apply_server_side_encryption_by_default"), "sse_algorithm", '"AES256"'),
    ],
    "aws_s3_bucket_public_access_block": [
        ((), "block_public_acls", "true"),
        ((), "block_public_policy", "true"),
        ((), "ignore_public_acls", "true"),
        ((), "restrict_public_buckets", "true"),
    ],
    "aws_security_group": [
        (("ingress",), "from_port", "443"),
        (("ingress",), "to_port", "443"),
        (("ingress",), "protocol", '"tcp"'),
        (("ingress",), "cidr_blocks", '["0.0.0.0/0"]'),
        (("egress",), "from_port", "0"),
        (("egress",), "to_port", "0"),
        (("egress",), "protocol", '"-1"'),
        (("egress",), "cidr_blocks", '["0.0.0.0/0"]'),
    ],
    "aws_lb_target_group": [(("health_check",), "path", '"/"')],
    "aws_cloudfront_distribution": [
        (("default_cache_behavior",), "viewer_protocol_policy", '"redirect-to-https"'),
        (("viewer_certificate",), "minimum_protocol_version", '"TLSv1.2_2021"'),
    ],
    "aws_instance": [(("metadata_options",), "http_tokens", '"required"')],
    "aws_launch_template": [(("metadata_options",), "http_tokens", '"required"')],
    "aws_dynamodb_table": [
        (("attribute",), "name", '"id"'),
        (("attribute",), "type", '"S"'),
        (("server_side_encryption",), "enabled", "true"),
        (("point_in_time_recovery",), "enabled", "true"),
    ],
    "aws_backup_plan": [
        (("rule",), "rule_name", '"daily"'),
        (("rule",), "target_vault_name", "aws_backup_vault.this.name"),
        (("rule",), "schedule", '"cron(0 5 ? * * *)"'),
    ],
    "aws_cognito_user_pool": [(("password_policy",), "minimum_length", "12")],
    "aws_wafv2_web_acl": [
        (("default_action", "allow"), "", ""),
    ],
    "aws_lambda_function": [
        (("environment",), "variables", '{ TABLE_NAME = "items" }'),
    ],
    "aws_apigatewayv2_integration": [
        ((), "integration_uri", "aws_lambda_function.this.invoke_arn"),
    ],
    "aws_apigatewayv2_route": [
        ((), "target", '"integrations/${aws_apigatewayv2_integration.this.id}"'),
    ],
    "aws_apigatewayv2_stage": [(("access_log_settings",), "destination_arn", "aws_cloudwatch_log_group.this.arn")],
    "aws_ecs_task_definition": [
        (
            (),
            "container_definitions",
            'jsonencode([{ name = "app", image = "nginx:alpine", essential = true }])',
        ),
    ],
    "aws_ecs_service": [
        (("network_configuration",), "subnets", "var.subnet_ids"),
        (("network_configuration",), "security_groups", "var.security_group_ids"),
    ],
    "aws_flow_log": [
        ((), "log_destination", "aws_cloudwatch_log_group.this.arn"),
        ((), "log_destination_type", '"cloud-watch-logs"'),
    ],
    "aws_cloudwatch_metric_alarm": [
        (("dimensions",), "InstanceId", "aws_instance.this.id"),
    ],
    "aws_route53_record": [
        (("alias",), "name", "aws_cloudfront_distribution.this.domain_name"),
        (("alias",), "zone_id", "aws_cloudfront_distribution.this.hosted_zone_id"),
    ],
    "aws_sns_topic_subscription": [
        ((), "topic_arn", "aws_sns_topic.this.arn"),
        ((), "endpoint", "aws_sqs_queue.this.arn"),
    ],
    "aws_lambda_permission": [
        ((), "function_name", "aws_lambda_function.this.function_name"),
        ((), "principal", '"apigateway.amazonaws.com"'),
    ],
    "aws_eip": [((), "instance", "aws_instance.this.id")],
    "aws_autoscaling_group": [
        (("launch_template",), "id", "aws_launch_template.this.id"),
        (("launch_template",), "version", '"$Latest"'),
    ],
    "docker_container": [
        (("ports",), "internal", "80"),
        (("ports",), "external", "8080"),
    ],
}

# Types that must be rendered as ``data`` blocks, never resources.
DATA_TYPES = {"aws_ami", "aws_iam_policy_document", "aws_region", "aws_caller_identity"}

DDB_POLICY = """jsonencode({
  Version = "2012-10-17"
  Statement = [
    {
      Effect   = "Allow"
      Action   = ["dynamodb:GetItem", "dynamodb:PutItem", "dynamodb:Query"]
      Resource = aws_dynamodb_table.this.arn
    }
  ]
})"""

DDB_ROLE_POLICY = """jsonencode({
  Version = "2012-10-17"
  Statement = [
    {
      Effect   = "Allow"
      Action   = ["dynamodb:GetItem"]
      Resource = aws_dynamodb_table.this.arn
    }
  ]
})"""

ASSUME_ROLE_POLICY = """jsonencode({
  Version = "2012-10-17"
  Statement = [
    {
      Effect    = "Allow"
      Principal = { Service = "lambda.amazonaws.com" }
      Action    = "sts:AssumeRole"
    }
  ]
})"""


# Which resource owns a textual marker.  Used to pick a focus and to decide
# where to inject a construct that only exists as a file_contains test.
MARKER_OWNER: dict[str, str] = {
    "0.0.0.0/0": "aws_route",
    "443": "aws_security_group",
    "Deny": "aws_s3_bucket_policy",
    "GET /items": "aws_apigatewayv2_route",
    "HTTPS": "aws_lb_listener",
    "TABLE_NAME": "aws_lambda_function",
    "aws:SecureTransport": "aws_s3_bucket_policy",
    "aws_acm_certificate.": "aws_cloudfront_distribution",
    "aws_backup_vault.": "aws_backup_plan",
    "aws_cloudwatch_log_group.": "aws_flow_log",
    "aws_instance.": "aws_eip_association",
    "aws_lambda_function.": "aws_cloudwatch_event_target",
    "aws_secretsmanager_secret.": "aws_db_instance",
    "aws_sns_topic.": "aws_cloudwatch_metric_alarm",
    "aws_sqs_queue.": "aws_sns_topic_subscription",
    "certificate_arn": "aws_lb_listener",
    "count.index": "aws_subnet",
    "cron(": "aws_backup_plan",
    "deadLetterTargetArn": "aws_sqs_queue",
    "depends_on": "aws_instance",
    "docker_network.": "docker_container",
    "dynamodb:": "aws_iam_policy",
    "each.": "aws_subnet",
    "invoke_arn": "aws_apigatewayv2_integration",
    "kms_master_key_id": "aws_s3_bucket_server_side_encryption_configuration",
    "lambda.amazonaws.com": "aws_iam_role",
    "lambda:InvokeFunction": "aws_lambda_permission",
    "local.": "aws_s3_bucket",
    "local.common_tags": "aws_s3_bucket",
    "redirect": "aws_lb_listener",
    "target_group_arn": "aws_lb_listener",
    "terraform.workspace": "locals",
    "var.subnet_cidrs": "aws_subnet",
    "vpc_security_group_ids": "aws_instance",
}

SPECIAL_MARKERS = {
    "backend \"s3\"",
    "bucket",
    "dynamodb_table",
    "encrypt",
    "for_each",
    "from",
    "id =",
    "import",
    "length(",
    "lifecycle",
    "locals",
    "merge(",
    "moved",
    "regex(",
    "sensitive",
    "source",
    "to",
    "to =",
    "true",
    "=",
    " ? ",
    ":",
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _indent(lines: Iterable[str], spaces: int) -> list[str]:
    pad = " " * spaces
    return [pad + line if line else line for line in lines]


def _literal(value: Any) -> str:
    """Render a Python value as an HCL expression."""
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, list):
        return "[" + ", ".join(_literal(v) for v in value) + "]"
    if isinstance(value, dict):
        body = ", ".join(f"{k} = {_literal(v)}" for k, v in value.items())
        return "{ " + body + " }"
    text = str(value)
    if text.startswith(("var.", "local.", "aws_", "data.", "docker_", "each.", "count.")):
        return text
    if text in ("true", "false", "null"):
        return text
    if re.fullmatch(r"-?\d+(\.\d+)?", text):
        return text
    escaped = text.replace('"', '\\"')
    return f'"{escaped}"'


def _ref_value(ref: str, attr: str) -> str:
    """Turn a challenge reference prefix into a concrete expression."""
    if ref and not ref.endswith("."):
        return ref
    if ref == "data.aws_ami.":
        return "data.aws_ami.latest.id"
    if ref.startswith("data."):
        return ref + "this.id"
    base = ref.rstrip(".")
    suffix = _ref_suffix(base, attr)
    return f"{base}.this.{suffix}"


def _ref_suffix(base: str, attr: str) -> str:
    if attr.endswith("_arn"):
        return "arn"
    if attr in ("target_group_arn", "load_balancer_arn", "policy_arn", "role_arn", "certificate_arn"):
        return "arn"
    if attr in ("vpc_id", "subnet_id", "route_table_id", "security_group_id", "instance_id"):
        return "id"
    if attr in ("name", "function_name", "role", "cluster", "task_definition", "target_vault_name", "db_subnet_group_name"):
        if base.endswith("task_definition"):
            return "arn"
        if base.endswith(("iam_role", "iam_policy")):
            return "arn"
        return "name" if base.endswith(("aws_db_subnet_group", "aws_iam_role")) else "id"
    if attr in ("invoke_arn", "integration_uri"):
        return "invoke_arn"
    if attr == "endpoint":
        return "endpoint"
    if attr == "zone_id":
        return "zone_id"
    if attr == "acm_certificate_arn":
        return "arn"
    if attr == "log_destination":
        return "arn"
    if attr == "domain_name":
        return "domain_name"
    if attr == "public_ip":
        return "public_ip"
    if attr in ("queue_url", "url"):
        return "url"
    if attr in ("table_name", "bucket_name", "queue_name"):
        return "name"
    if base.endswith("aws_s3_bucket"):
        return "id"
    if base.endswith(("aws_acm_certificate", "aws_kms_key", "aws_sns_topic", "aws_sqs_queue", "aws_cloudwatch_log_group", "aws_backup_vault", "aws_backup_plan", "aws_lambda_function", "aws_lb", "aws_lb_target_group", "aws_iam_role", "aws_iam_policy")):
        return "arn"
    return "id"


def _tag_value(expected: str) -> str:
    return expected


def _tags_block(expected: dict[str, str], indent: str = "  ") -> list[str]:
    lines = ["tags = {"]
    for key, value in expected.items():
        lines.append(f"  {key} = {_tag_value(value)}")
    lines.append("}")
    return [indent + line for line in lines]


def _provider_required() -> list[str]:
    return [
        "required_providers {",
        "  aws = {",
        '    source  = "hashicorp/aws"',
        '    version = "~> 5.0"',
        "  }",
        "}",
    ]


def _provider_docker() -> list[str]:
    return [
        "required_providers {",
        "  docker = {",
        '    source  = "kreuzwerker/docker"',
        '    version = "~> 3.0"',
        "  }",
        "}",
    ]


def _needs_aws(spec: dict) -> bool:
    text = " ".join(
        [spec.get("id", "")]
        + [str(x) for x in spec.get("expected_resources", [])]
        + [str(x) for x in spec.get("allowlist", [])]
    )
    return "aws_" in text or "aws" in spec.get("tags", []) or spec.get("id", "").startswith(
        ("provision-", "harden-", "wire-")
    )


def _needs_docker(spec: dict) -> bool:
    text = spec.get("id", "") + " " + " ".join(spec.get("tags", []))
    return "docker" in text


def _effective_variables(spec: dict) -> list[dict]:
    """Spec variables plus implicit support variables used by tags/providers."""
    out: list[dict] = [dict(v) for v in spec.get("variables", [])]
    names = {v["name"] for v in out}
    refs: set[str] = set()
    for test in spec.get("tests", []):
        check = test.get("check", {})
        for key in ("ref", "value"):
            val = check.get(key)
            if isinstance(val, str):
                refs.update(re.findall(r"\bvar\.([A-Za-z_][A-Za-z0-9_]*)", val))
        for val in check.get("tags", {}).values():
            if isinstance(val, str):
                refs.update(re.findall(r"\bvar\.([A-Za-z_][A-Za-z0-9_]*)", val))
    if _needs_aws(spec):
        refs.add("aws_region")
    # Tag tests use the standard project/environment names.
    if any(t.get("check", {}).get("kind") in ("tagged", "all_tagged") for t in spec.get("tests", [])):
        refs.update({"project_name", "environment"})
    defaults = {
        "aws_region": ("string", "us-east-1"),
        "project_name": ("string", "terraform-practice"),
        "environment": ("string", "dev"),
        "docker_host": ("string", "unix:///var/run/docker.sock"),
    }
    for name in sorted(refs):
        if name in names:
            continue
        type_, default = defaults.get(name, ("string", ""))
        out.append(
            {
                "name": name,
                "type": type_,
                "validation": False,
                "default": default,
                "_implicit": True,
            }
        )
        names.add(name)
    return out


# ---------------------------------------------------------------------------
# Focus selection
# ---------------------------------------------------------------------------
EXPLICIT_FOCUS: dict[str, dict] = {
    "lang-variables-validation": {
        "kind": "validation",
        "file": "variables.tf",
        "var": "bucket_name",
        "title": "Complete the validation block for bucket_name",
        "todo": "Add a condition and error_message that enforce the documented bucket naming rules.",
    },
    "lang-locals-common-tags": {
        "kind": "top",
        "file": "main.tf",
        "block": "locals",
        "title": "Complete the shared tags locals block",
        "todo": "Define local.common_tags and merge the standard tags into it.",
    },
    "lang-count-subnets": {
        "kind": "resource",
        "file": "main.tf",
        "rtype": "aws_subnet",
        "name": "this",
        "title": "Complete the aws_subnet block",
        "todo": "Use count and the subnet CIDR list so one subnet is created per entry.",
    },
    "lang-for-each-subnets": {
        "kind": "resource",
        "file": "main.tf",
        "rtype": "aws_subnet",
        "name": "this",
        "title": "Complete the aws_subnet block",
        "todo": "Use for_each over the subnet map and reference each.key/value.",
    },
    "lang-conditional-environment": {
        "kind": "attr",
        "file": "main.tf",
        "rtype": "aws_s3_bucket",
        "name": "this",
        "path": (),
        "attr": "bucket",
        "title": "Complete the bucket name expression",
        "todo": "Use a conditional expression so production keeps the base name and other environments get a suffix.",
    },
    "lang-functions-merge": {
        "kind": "top",
        "file": "main.tf",
        "block": "locals",
        "title": "Complete the locals block",
        "todo": "Build local.common_tags with merge() and reuse it on the bucket.",
    },
    "lang-data-sources": {
        "kind": "top",
        "file": "main.tf",
        "block": "data",
        "name": "latest",
        "title": "Complete the aws_ami data source",
        "todo": "Add most_recent, owners and a filter so the newest Amazon Linux image is discovered.",
    },
    "lang-sensitive-output": {
        "kind": "output_attr",
        "file": "outputs.tf",
        "output": "bucket_arn",
        "attr": "sensitive",
        "title": "Mark the output as sensitive",
        "todo": "Add the sensitive argument to the bucket_arn output.",
    },
    "lang-lifecycle-protect": {
        "kind": "nested",
        "file": "main.tf",
        "rtype": "aws_s3_bucket",
        "name": "this",
        "path": ("lifecycle",),
        "title": "Complete the lifecycle block",
        "todo": "Protect the bucket from accidental deletion with prevent_destroy.",
    },
    "lang-depends-on": {
        "kind": "attr",
        "file": "main.tf",
        "rtype": "aws_instance",
        "name": "this",
        "path": (),
        "attr": "depends_on",
        "title": "Add the explicit dependency",
        "todo": "Make the instance wait for the security group with depends_on.",
    },
    "mod-local-module": {
        "kind": "top",
        "file": "main.tf",
        "block": "module",
        "name": "this",
        "title": "Complete the module call",
        "todo": "Point the module at ./modules/s3 and pass the bucket inputs.",
    },
    "mod-module-for-each": {
        "kind": "top",
        "file": "main.tf",
        "block": "module",
        "name": "this",
        "title": "Complete the for_each module call",
        "todo": "Instantiate the module once per environment with for_each.",
    },
    "state-s3-backend": {
        "kind": "backend",
        "file": "versions.tf",
        "title": "Complete the S3 backend configuration",
        "todo": "Fill in the state bucket, key, region, DynamoDB lock table and encryption flag.",
    },
    "state-workspaces": {
        "kind": "top",
        "file": "main.tf",
        "block": "locals",
        "title": "Complete the workspace-aware locals block",
        "todo": "Derive the bucket name from terraform.workspace and reuse it on the bucket.",
    },
    "refactor-moved-block": {
        "kind": "top",
        "file": "main.tf",
        "block": "moved",
        "title": "Complete the moved block",
        "todo": "Declare the old and new resource addresses so Terraform preserves state.",
    },
    "import-block": {
        "kind": "top",
        "file": "main.tf",
        "block": "import",
        "title": "Complete the import block",
        "todo": "Give the real bucket id and the Terraform address it should be imported to.",
    },
    "harden-sqs-dlq": {
        "kind": "resource",
        "file": "main.tf",
        "rtype": "aws_sqs_queue",
        "name": "this",
        "title": "Complete the main queue",
        "todo": "Add the queue name, server-side encryption and redrive policy pointing at the DLQ.",
    },
    "harden-alb-https": {
        "kind": "resource",
        "file": "main.tf",
        "rtype": "aws_lb_listener",
        "name": "https",
        "title": "Complete the HTTPS listener",
        "todo": "Configure the 443/HTTPS listener with the certificate and a forward action.",
    },
    "docker-multi-container": {
        "kind": "resource",
        "file": "main.tf",
        "rtype": "docker_network",
        "name": "this",
        "title": "Complete the shared Docker network",
        "todo": "Create the network that both containers join.",
    },
    "wire-eventbridge-lambda": {
        "kind": "resource",
        "file": "main.tf",
        "rtype": "aws_lambda_function",
        "name": "this",
        "title": "Complete the scheduled function",
        "todo": "Configure the function runtime, handler, role and memory for the scheduled job.",
    },
}


def _check_score(spec: dict, rtype: str) -> int:
    score = 0
    for test in spec.get("tests", []):
        check = test.get("check", {})
        if check.get("resource") == rtype:
            if check.get("kind") in ("attr_ref", "attr_equals", "attr_present", "attr_contains"):
                score += 2
            elif str(check.get("kind", "")).startswith("nested"):
                score += 2
        if check.get("kind") == "file_contains" and MARKER_OWNER.get(check.get("text")) == rtype:
            score += 3
    return score


def choose_focus(spec: dict) -> Focus:
    explicit = spec.get("focus") or EXPLICIT_FOCUS.get(spec.get("id", ""))
    if explicit:
        return Focus(**explicit)

    expected = [r for r in spec.get("expected_resources", []) if r not in ("module", "data")]
    candidates = expected[:]
    for test in spec.get("tests", []):
        check = test.get("check", {})
        for key in ("resource", "type"):
            if key in check and check[key] not in ("module", "data"):
                candidates.append(check[key])
        candidates.extend(check.get("resources", []))
    # Preserve order, drop duplicates and non-resource values.
    ordered: list[str] = []
    for rtype in candidates:
        if rtype and rtype not in ordered and rtype.startswith(("aws_", "docker_")):
            ordered.append(rtype)
    if not ordered:
        return Focus(kind="top", file="main.tf", block="locals", title="Complete the configuration")

    best = max(ordered, key=lambda r: (_check_score(spec, r), -ordered.index(r)))
    return Focus(
        kind="resource",
        file="main.tf",
        rtype=best,
        name="this",
        title=f"Complete the {best} resource",
        todo=f"Add the arguments and nested blocks required for {best}.",
    )


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------
def _focus_matches_res(focus: Focus, res: Res, kind: str) -> bool:
    return (
        focus.kind == kind
        and focus.file == "main.tf"
        and focus.rtype == res.rtype
        and focus.name == res.name
    )


def _bracket_delta(text: str) -> int:
    """Net ``{``/``[`` depth change, ignoring quoted strings.

    Terraform's formatter indents continuation lines by the nesting of objects
    and lists, not by function-call parentheses.  Ignoring parentheses makes
    ``jsonencode({ ... })`` line up the way ``terraform fmt`` expects.
    """
    depth = 0
    in_string = False
    escaped = False
    for char in text:
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            continue
        if char == '"':
            in_string = True
        elif char in "{[":
            depth += 1
        elif char in "}]":
            depth -= 1
    return depth


def _attr_lines(indent: str, name: str, value: str) -> list[str]:
    parts = str(value).split("\n")
    out = [f"{indent}{name} = {parts[0]}"]
    if len(parts) == 1:
        return out

    depth = max(0, _bracket_delta(parts[0]))
    for part in parts[1:]:
        stripped = part.strip()
        if not stripped:
            out.append("")
            continue
        # A line that starts with closing brackets prints one level out for
        # each leading closer, but those closers must only be counted once.
        # Apply the full line delta afterwards so ``]`` and ``})`` stay aligned
        # with the line that opened them, the way ``terraform fmt`` does.
        leading = 0
        while leading < len(stripped) and stripped[leading] in "}]":
            leading += 1
        print_depth = max(0, depth - leading)
        out.append(f"{indent}{'  ' * print_depth}{stripped}")
        depth = max(0, depth + _bracket_delta(stripped))
    return out


_ATTR_LINE = re.compile(
    r'^(\s*)("(?:[^"\\]|\\.)*"|[A-Za-z_][\w-]*)\s*=\s*(.*)$'
)


def canonicalize_hcl(text: str) -> str:
    """Apply the two formatting rules ``terraform fmt`` uses most often here.

    * continuation lines inside multi-line values are re-indented by structural
      depth (handled in ``_attr_lines`` when the text is generated);
    * consecutive single-line attributes at the same indentation align their
      ``=`` signs.

    The alignment pass runs on complete files, so it also catches hand-authored
    references and object/list entries inside a multi-line value.
    """
    lines = text.split("\n")
    out: list[str] = []
    index = 0
    while index < len(lines):
        match = _ATTR_LINE.match(lines[index])
        if not match:
            out.append(lines[index])
            index += 1
            continue

        indent = match.group(1)
        group: list[tuple[str, str]] = []
        cursor = index
        while cursor < len(lines):
            candidate = _ATTR_LINE.match(lines[cursor])
            if not candidate or candidate.group(1) != indent:
                break
            value = candidate.group(3)
            if _bracket_delta(value) > 0:
                break
            group.append((candidate.group(2), value))
            cursor += 1

        if len(group) < 2:
            out.append(lines[index])
            index += 1
            continue

        width = max(len(name) for name, _ in group)
        for name, value in group:
            out.append(f"{indent}{name:<{width}} = {value}")
        index = cursor
    return "\n".join(out)


def canonicalize_files(files: dict[str, str]) -> dict[str, str]:
    return {name: canonicalize_hcl(text) for name, text in files.items()}


def _render_node(
    node: Node,
    indent: str,
    focus: Focus | None,
    res: Res | None = None,
    path: tuple[str, ...] = (),
    wrap_all: bool = False,
) -> list[str]:
    lines: list[str] = []
    done = False
    for name, value in node.attrs.items():
        attr_lines = _attr_lines(indent, name, value)
        if (
            not wrap_all
            and not done
            and focus is not None
            and res is not None
            and focus.kind == "attr"
            and focus.attr == name
            and focus.path == path
        ):
            lines.append(f"{indent}{FOCUS_START}")
            lines.extend(attr_lines)
            lines.append(f"{indent}{FOCUS_END}")
            done = True
        else:
            lines.extend(attr_lines)
    for block_name, children in node.blocks.items():
        for index, child in enumerate(children):
            lines.append(f"{indent}{block_name} {{")
            nested_focus = focus
            nested_wrap = wrap_all
            if (
                not wrap_all
                and not done
                and focus is not None
                and res is not None
                and focus.kind == "nested"
                and focus.path == path + (block_name,)
                and index == 0
            ):
                nested_focus = None
                nested_wrap = True
            body = _render_node(child, indent + "  ", nested_focus, res, path + (block_name,), nested_wrap)
            if nested_wrap:
                body = [f"{indent}  {FOCUS_START}"] + body + [f"{indent}  {FOCUS_END}"]
                done = True
            lines.extend(body)
            lines.append(f"{indent}}}")
    return lines


def _render_res(res: Res, focus: Focus) -> list[str]:
    header = f'{res.kind} "{res.rtype}" "{res.name}" {{'
    resource_focus = _focus_matches_res(focus, res, "resource")
    nested_focus = focus if _focus_matches_res(focus, res, "nested") or _focus_matches_res(focus, res, "attr") else None
    body = _render_node(res.root, "  ", nested_focus, res, ())
    if resource_focus:
        body = ["  " + FOCUS_START] + body + ["  " + FOCUS_END]
    if not body:
        return [header, "}"]
    return [header] + body + ["}"]


def _render_top_block(
    block_type: str,
    labels: list[str],
    node: Node,
    focus: Focus,
    *,
    match: bool = False,
) -> list[str]:
    header = block_type
    if labels:
        header += " " + " ".join(f'"{label}"' for label in labels)
    header += " {"
    body = _render_node(node, "  ", None)
    if match:
        body = ["  " + FOCUS_START] + body + ["  " + FOCUS_END]
    return [header] + body + ["}"]


# ---------------------------------------------------------------------------
# Resource synthesis
# ---------------------------------------------------------------------------
def _resource_types(spec: dict) -> list[str]:
    types: list[str] = []
    for rtype in spec.get("expected_resources", []):
        if rtype not in types and rtype.startswith(("aws_", "docker_")) and rtype not in DATA_TYPES:
            types.append(rtype)
    for test in spec.get("tests", []):
        check = test.get("check", {})
        for key in ("resource", "type"):
            value = check.get(key)
            if value and value.startswith(("aws_", "docker_")) and value not in DATA_TYPES and value not in types:
                types.append(value)
        for value in check.get("resources", []):
            if value.startswith(("aws_", "docker_")) and value not in DATA_TYPES and value not in types:
                types.append(value)
        if check.get("kind") == "file_contains":
            owner = MARKER_OWNER.get(check.get("text"))
            if owner and owner.startswith(("aws_", "docker_")) and owner not in DATA_TYPES and owner not in types:
                types.append(owner)
    return types


def _data_types(spec: dict) -> list[str]:
    found: list[str] = []
    sid = spec.get("id", "")
    if sid == "lang-data-sources":
        found.append("aws_ami")
    for test in spec.get("tests", []):
        check = test.get("check", {})
        if check.get("kind") == "data_exists":
            value = check.get("type")
            if value and value not in found:
                found.append(value)
    return found


def _special_resource_names(spec: dict) -> dict[str, list[str]]:
    sid = spec.get("id", "")
    if sid == "harden-sqs-dlq":
        return {"aws_sqs_queue": ["this", "dlq"]}
    if sid == "harden-alb-https":
        return {"aws_lb_listener": ["https", "http"]}
    if sid == "docker-multi-container":
        return {"docker_container": ["web", "worker"]}
    return {}


def _add_tags(res: Res, tags: dict[str, str], *, use_local: bool = False) -> None:
    if use_local:
        res.attr("tags", "local.common_tags")
        return
    if not tags:
        return
    # Inline the map so effective_tags can resolve it without a locals block.
    body = ["{"]
    for key, value in tags.items():
        body.append(f"  {key} = {value}")
    body.append("}")
    res.attr("tags", "\n".join(body))


def _build_resources(spec: dict) -> dict[str, list[Res]]:
    types = _resource_types(spec)
    special_names = _special_resource_names(spec)
    result: dict[str, list[Res]] = {}
    checks = [t.get("check", {}) for t in spec.get("tests", [])]

    for rtype in types:
        names = special_names.get(rtype, ["this"])
        for name in names:
            res = Res(rtype, name)
            # Required defaults first.
            for attr, value in RESOURCE_DEFAULTS.get(rtype, []):
                res.ensure(attr, value)
            for path, attr, value in NESTED_DEFAULTS.get(rtype, []):
                if not path and not attr:
                    res.block(path[0])
                elif not attr:
                    res.block(path[0])
                else:
                    res.block(path[0]) if len(path) == 1 else res.root.path(*path)
                    target = res.root if not path else res.root.path(*path)
                    target.setdefault(attr, value)
            # Tag tests.
            for check in checks:
                if check.get("kind") == "tagged" and rtype in check.get("resources", []):
                    _add_tags(res, check.get("tags", {}))
                if check.get("kind") == "all_tagged":
                    _add_tags(res, check.get("tags", {}))
            # Attribute / nested checks for this resource.  Only the first
            # block of a type receives the asserted attributes; secondary
            # blocks get sensible defaults only.
            if name == names[0]:
                for check in checks:
                    if check.get("resource") != rtype:
                        continue
                    kind = check.get("kind")
                    if kind == "attr_ref":
                        res.attr(check["attr"], _ref_value(check["ref"], check["attr"]))
                    elif kind == "attr_equals":
                        res.attr(check["attr"], str(check["value"]))
                    elif kind == "attr_present":
                        res.ensure(check["attr"], _attr_default(rtype, check["attr"]))
                    elif kind == "attr_contains":
                        res.attr(check["attr"], str(check["text"]))
                    elif kind in ("attr_number_max", "attr_number_min"):
                        res.attr(check["attr"], str(check["value"]))
                    elif kind == "nested_path":
                        node = res.root.path(*check["path"])
                        node.set(check["attr"], str(check["value"]))
                    elif kind == "nested_path_max":
                        node = res.root.path(*check["path"])
                        node.attr(check["attr"], str(check["value"])) if False else node.set(check["attr"], str(check["value"]))
                    elif kind == "nested_path_present":
                        res.root.path(*check["path"])
                    elif kind == "nested_present":
                        node = res.block(check["block"])
                        if check.get("attr"):
                            node.ensure(check["attr"], _attr_default(rtype, check["attr"]))
                    elif kind == "nested_equals":
                        node = res.block(check["block"])
                        node.set(check["attr"], str(check["value"]))
                    elif kind == "nested_ref":
                        node = res.block(check["block"])
                        node.set(check["attr"], _ref_value(check["ref"], check["attr"]))
                    elif kind == "nested_count_min":
                        for _ in range(check.get("min", 1)):
                            res.add_block(check["block"])
                    elif kind == "count_or_foreach":
                        # Filled by the marker handlers below.
                        pass
            result.setdefault(rtype, []).append(res)

    _apply_marker_handlers(spec, result)
    _apply_special_resource_shapes(spec, result)
    if "aws_iam_policy_document" in _data_types(spec):
        policy = _first(result, "aws_iam_policy")
        if policy is not None:
            policy.attr("policy", "data.aws_iam_policy_document.this.json")
    return result


def _attr_default(rtype: str, attr: str) -> str:
    if attr.endswith("_arn"):
        return f"{rtype}.this.arn"
    if attr == "assume_role_policy":
        return ASSUME_ROLE_POLICY
    if attr == "policy":
        return DDB_POLICY if rtype == "aws_iam_policy" else 'jsonencode({ Version = "2012-10-17", Statement = [] })'
    if attr == "definition":
        return 'jsonencode({ Version = "2012-10-17", Statement = [] })'
    if attr in ("name", "bucket", "identifier", "function_name"):
        return '"app-asset"'
    return '"example"'


def _first(resources: dict[str, list[Res]], rtype: str) -> Res | None:
    items = resources.get(rtype)
    return items[0] if items else None


def _apply_marker_handlers(spec: dict, resources: dict[str, list[Res]]) -> None:
    markers = {
        t["check"].get("text")
        for t in spec.get("tests", [])
        if t.get("check", {}).get("kind") == "file_contains"
    }
    for marker in markers:
        if not marker:
            continue
        owner = MARKER_OWNER.get(marker)
        if marker == "target_group_arn":
            for listener in resources.get("aws_lb_listener", []):
                action = listener.block("default_action")
                action.setdefault("type", '"forward"')
                action.set("target_group_arn", "aws_lb_target_group.this.arn")
        elif marker == "HTTPS":
            listeners = resources.get("aws_lb_listener", [])
            if listeners:
                listeners[0].attr("protocol", '"HTTPS"')
                listeners[0].attr("port", "443")
        elif marker == "certificate_arn":
            listeners = resources.get("aws_lb_listener", [])
            if listeners:
                listeners[0].attr("certificate_arn", "var.certificate_arn")
        elif marker == "redirect":
            listeners = resources.get("aws_lb_listener", [])
            target = listeners[1] if len(listeners) > 1 else (listeners[0] if listeners else None)
            if target:
                action = target.block("default_action")
                action.setdefault("type", '"redirect"')
                redirect = action.child("redirect")
                redirect.setdefault("port", '"443"')
                redirect.setdefault("protocol", '"HTTPS"')
                redirect.setdefault("status_code", '"HTTP_301"')
        elif marker == "deadLetterTargetArn":
            queue = _first(resources, "aws_sqs_queue")
            if queue:
                queue.attr(
                    "redrive_policy",
                    'jsonencode({ deadLetterTargetArn = aws_sqs_queue.dlq.arn, maxReceiveCount = 3 })',
                )
        elif marker == "dynamodb:":
            policy = _first(resources, "aws_iam_policy")
            if policy:
                policy.attr("policy", DDB_POLICY)
            role_policy = _first(resources, "aws_iam_role_policy")
            if role_policy:
                role_policy.attr("policy", DDB_ROLE_POLICY)
        elif marker == "lambda.amazonaws.com":
            role = _first(resources, "aws_iam_role")
            if role:
                role.attr("assume_role_policy", ASSUME_ROLE_POLICY)
        elif marker == " ? ":
            bucket = _first(resources, "aws_s3_bucket")
            if bucket:
                bucket.attr(
                    "bucket",
                    'var.environment == "prod" ? var.bucket_name : "${var.bucket_name}-${var.environment}"',
                )
        elif marker == "lambda:InvokeFunction":
            perm = _first(resources, "aws_lambda_permission")
            if perm:
                perm.attr("action", '"lambda:InvokeFunction"')
                perm.attr("principal", '"apigateway.amazonaws.com"')
                perm.attr("function_name", "aws_lambda_function.this.function_name")
        elif marker == "invoke_arn":
            integration = _first(resources, "aws_apigatewayv2_integration")
            if integration:
                integration.attr("integration_uri", "aws_lambda_function.this.invoke_arn")
        elif marker == "GET /items":
            route = _first(resources, "aws_apigatewayv2_route")
            if route:
                route.attr("route_key", '"GET /items"')
                route.attr(
                    "target",
                    '"integrations/${aws_apigatewayv2_integration.this.id}"',
                )
        elif marker == "TABLE_NAME":
            fn = _first(resources, "aws_lambda_function")
            if fn:
                env = fn.block("environment")
                env.set("variables", '{ TABLE_NAME = aws_dynamodb_table.this.name }')
        elif marker == "aws_instance.":
            assoc = _first(resources, "aws_eip_association")
            if assoc:
                assoc.attr("instance_id", "aws_instance.this.id")
            eip = _first(resources, "aws_eip")
            if eip:
                eip.attr("instance", "aws_instance.this.id")
        elif marker == "aws_sns_topic.":
            alarm = _first(resources, "aws_cloudwatch_metric_alarm")
            if alarm:
                alarm.attr("alarm_actions", "[aws_sns_topic.this.arn]")
        elif marker == "aws_sqs_queue.":
            sub = _first(resources, "aws_sns_topic_subscription")
            if sub:
                sub.attr("endpoint", "aws_sqs_queue.this.arn")
        elif marker == "aws_lambda_function.":
            target = _first(resources, "aws_cloudwatch_event_target")
            if target:
                target.attr("arn", "aws_lambda_function.this.arn")
                target.attr("input", 'jsonencode({})')
        elif marker == "aws_cloudwatch_log_group.":
            flow = _first(resources, "aws_flow_log")
            if flow:
                flow.attr("log_destination", "aws_cloudwatch_log_group.this.arn")
        elif marker == "aws_acm_certificate.":
            cf = _first(resources, "aws_cloudfront_distribution")
            if cf:
                cert = cf.block("viewer_certificate")
                cert.set("acm_certificate_arn", "aws_acm_certificate.this.arn")
                cert.setdefault("ssl_support_method", '"sni-only"')
        elif marker == "aws_backup_vault.":
            plan = _first(resources, "aws_backup_plan")
            if plan:
                plan.root.path("rule").set("target_vault_name", "aws_backup_vault.this.name")
        elif marker == "cron(":
            plan = _first(resources, "aws_backup_plan")
            if plan:
                plan.root.path("rule").set("schedule", '"cron(0 5 ? * * *)"')
                plan.root.path("rule").setdefault("schedule_expression", '"cron(0 5 ? * * *)"')
        elif marker == "aws_secretsmanager_secret.":
            db = _first(resources, "aws_db_instance")
            if db:
                existing = db.root.attrs.get("tags")
                secret_tag = "Secret = aws_secretsmanager_secret.this.arn"
                if existing:
                    db.attr("tags", existing.replace("}", f"  {secret_tag}\n}}"))
                else:
                    db.attr("tags", "{\n  " + secret_tag + "\n}")
        elif marker == "kms_master_key_id":
            sse = _first(resources, "aws_s3_bucket_server_side_encryption_configuration")
            if sse:
                sse.root.path("rule", "apply_server_side_encryption_by_default").set(
                    "kms_master_key_id", "aws_kms_key.this.arn"
                )
        elif marker in ("aws:SecureTransport", "Deny"):
            policy = _first(resources, "aws_s3_bucket_policy")
            if policy:
                policy.attr(
                    "policy",
                    'jsonencode({ Version = "2012-10-17", Statement = [{ Effect = "Deny", Principal = "*", Action = "s3:*", Resource = [aws_s3_bucket.this.arn, "${aws_s3_bucket.this.arn}/*"], Condition = { Bool = { "aws:SecureTransport" = "false" } } }] })',
                )
        elif marker == "0.0.0.0/0":
            route = _first(resources, "aws_route")
            if route:
                route.attr("destination_cidr_block", '"0.0.0.0/0"')
                route.attr("gateway_id", "aws_internet_gateway.this.id")
        elif marker == "443":
            sg = _first(resources, "aws_security_group")
            if sg:
                ingress = sg.block("ingress")
                ingress.set("from_port", "443")
                ingress.set("to_port", "443")
                ingress.setdefault("protocol", '"tcp"')
                ingress.setdefault("cidr_blocks", '["0.0.0.0/0"]')
        elif marker == "vpc_security_group_ids":
            instance = _first(resources, "aws_instance")
            if instance:
                instance.attr("vpc_security_group_ids", "[aws_security_group.this.id]")
        elif marker == "depends_on":
            instance = _first(resources, "aws_instance")
            if instance:
                instance.attr("depends_on", "[aws_security_group.this]")
        elif marker in ("count.index", "var.subnet_cidrs"):
            subnet = _first(resources, "aws_subnet")
            if subnet:
                subnet.attr("count", "length(var.subnet_cidrs)")
                subnet.attr("vpc_id", "var.vpc_id")
                subnet.attr("cidr_block", "var.subnet_cidrs[count.index]")
                subnet.attr("availability_zone", "var.availability_zones[count.index]")
        elif marker in ("for_each", "each."):
            subnet = _first(resources, "aws_subnet")
            if subnet:
                subnet.attr("for_each", "var.subnets")
                subnet.attr("vpc_id", "var.vpc_id")
                subnet.attr("cidr_block", "each.value")
                subnet.attr("availability_zone", "each.key")
        elif marker == "lifecycle":
            bucket = _first(resources, "aws_s3_bucket")
            if bucket:
                lifecycle = bucket.block("lifecycle")
                lifecycle.setdefault("prevent_destroy", "true")
        elif marker == "docker_network.":
            for container in resources.get("docker_container", []):
                network = container.block("networks_advanced")
                network.set("name", "docker_network.this.name")
        elif marker == "source" or marker == "=":
            pass  # module special block
        # Other markers (locals, merge, regex, sensitive, backend, moved,
        # import, terraform.workspace, etc.) are handled by the special-block
        # renderers below.


def _apply_special_resource_shapes(spec: dict, resources: dict[str, list[Res]]) -> None:
    """Give multi-instance resources realistic, distinct values."""
    sid = spec.get("id", "")
    if sid == "harden-sqs-dlq":
        queues = resources.get("aws_sqs_queue", [])
        if len(queues) > 1:
            queues[0].attr("name", "var.queue_name")
            queues[1].attr("name", "var.dlq_name")
    elif sid == "harden-alb-https":
        listeners = resources.get("aws_lb_listener", [])
        if len(listeners) > 1:
            listeners[0].attr("port", "443")
            listeners[0].attr("protocol", '"HTTPS"')
            listeners[0].attr("certificate_arn", "var.certificate_arn")
            listeners[0].attr("load_balancer_arn", "var.lb_arn")
            listeners[0].block("default_action").setdefault("type", '"forward"')
            listeners[0].block("default_action").set(
                "target_group_arn", "var.target_group_arn"
            )
            listeners[1].attr("port", "80")
            listeners[1].attr("protocol", '"HTTP"')
            listeners[1].attr("load_balancer_arn", "var.lb_arn")
            action = listeners[1].block("default_action")
            action.set("type", '"redirect"')
            redirect = action.child("redirect")
            redirect.set("port", '"443"')
            redirect.set("protocol", '"HTTPS"')
            redirect.set("status_code", '"HTTP_301"')
    elif sid == "docker-multi-container":
        containers = resources.get("docker_container", [])
        names = ["web", "worker"]
        images = ["nginx:alpine", "alpine:latest"]
        for index, container in enumerate(containers):
            container.attr("name", f'"${{var.network_name}}-{names[index]}"')
            container.attr("image", f'"{images[index]}"')
            network = container.block("networks_advanced")
            network.set("name", "docker_network.this.name")


# ---------------------------------------------------------------------------
# Special top-level blocks
# ---------------------------------------------------------------------------
def _locals_common_tags() -> Node:
    root = Node()
    root.set(
        "common_tags",
        "merge(\n"
        "    {\n"
        "      Project     = var.project_name\n"
        "      Environment = var.environment\n"
        "    },\n"
        "    {\n"
        '      ManagedBy = "terraform"\n'
        "    }\n"
        "  )",
    )
    return root


def _locals_workspace() -> Node:
    root = Node()
    root.set("bucket_name", '"app-assets-${terraform.workspace}"')
    return root


def _data_ami() -> Node:
    root = Node()
    root.set("most_recent", "true")
    root.set("owners", '["amazon"]')
    filt = root.child("filter")
    filt.set("name", '\"name\"')
    filt.set("values", '["al2023-ami-*-x86_64"]')
    return root


def _data_policy_document() -> Node:
    root = Node()
    statement = root.child("statement")
    statement.set("sid", '\"DynamoDbReadWrite\"')
    statement.set("effect", '\"Allow\"')
    statement.set("actions", '[\"dynamodb:GetItem\", \"dynamodb:PutItem\", \"dynamodb:Query\"]')
    statement.set("resources", '[\"${aws_dynamodb_table.this.arn}\"]')
    return root


def _data_node(dtype: str) -> Node:
    if dtype == "aws_ami":
        return _data_ami()
    if dtype == "aws_iam_policy_document":
        return _data_policy_document()
    if dtype == "aws_caller_identity":
        return Node()
    if dtype == "aws_region":
        return Node()
    return Node()


def _module_block(spec: dict) -> Node:
    root = Node()
    root.set("source", '"./modules/s3"')
    if spec.get("id") == "mod-module-for-each":
        root.set("for_each", "{\n    dev  = \"dev\"\n    prod = \"prod\"\n  }")
        root.set("bucket_name", '"app-assets-${each.key}"')
        root.set("environment", "each.value")
    else:
        root.set("bucket_name", '"app-assets"')
        root.set("environment", '"dev"')
    return root


def _moved_block() -> Node:
    root = Node()
    root.set("from", "aws_s3_bucket.old")
    root.set("to", "aws_s3_bucket.new")
    return root


def _import_block() -> Node:
    root = Node()
    root.set("id", '"imported-assets"')
    root.set("to", "aws_s3_bucket.this")
    return root


def _backend_block() -> Node:
    root = Node()
    root.set("bucket", '"arena-terraform-state"')
    root.set("key", '"practice/terraform.tfstate"')
    root.set("region", '"us-east-1"')
    root.set("dynamodb_table", '"arena-terraform-locks"')
    root.set("encrypt", "true")
    return root


# ---------------------------------------------------------------------------
# File assembly
# ---------------------------------------------------------------------------
def _render_variables(variables: list[dict], focus: Focus) -> str:
    lines: list[str] = []
    for var in variables:
        name = var["name"]
        lines.append(f'variable "{name}" {{')
        lines.append(f'  description = "Input variable {name}."')
        lines.append(f'  type        = {var.get("type", "string")}')
        if "default" in var and not var.get("_implicit_no_default"):
            default = var["default"]
            if isinstance(default, str) and default.startswith(("var.", "local.")):
                lines.append(f"  default     = {default}")
            else:
                lines.append(f"  default     = {_literal(default)}")
        if var.get("validation"):
            lines.append("  validation {")
            condition = (
                'length(var.bucket_name) >= 3 && length(var.bucket_name) <= 63 && '
                'can(regex("^[a-z0-9-]+$", var.bucket_name))'
            )
            error = "Use 3-63 lowercase letters, numbers, or hyphens."
            body = [
                f"    condition     = {condition}",
                f'    error_message = "{error}"',
            ]
            if focus.kind == "validation" and focus.var == name:
                lines.append("    " + FOCUS_START)
                lines.extend(body)
                lines.append("    " + FOCUS_END)
            else:
                lines.extend(body)
            lines.append("  }")
        lines.append("}")
        lines.append("")
    while lines and lines[-1] == "":
        lines.pop()
    return "\n".join(lines) + ("\n" if lines else "")


def _output_ref_value(spec: dict, name: str, ref: str) -> str:
    if spec.get("id") == "harden-alb-https" and name == "listener_arn":
        return "aws_lb_listener.https.arn"
    return _ref_value(ref, name)


def _render_outputs(spec: dict, focus: Focus) -> str:
    outputs: OrderedDict[str, str] = OrderedDict()
    for test in spec.get("tests", []):
        check = test.get("check", {})
        if check.get("kind") == "output_ref":
            ref = check.get("ref") or "aws_s3_bucket."
            outputs.setdefault(check["name"], _output_ref_value(spec, check["name"], ref))
        elif check.get("kind") == "output_exists":
            outputs.setdefault(check["name"], '"sensitive-value"')
    for name in spec.get("expected_outputs", []):
        outputs.setdefault(name, _output_fallback(spec, name))
    lines: list[str] = []
    for name, value in outputs.items():
        lines.append(f'output "{name}" {{')
        lines.append(f"  value = {value}")
        if focus.kind == "output_attr" and focus.output == name and focus.attr == "sensitive":
            lines.append("  " + FOCUS_START)
            lines.append("  sensitive = true")
            lines.append("  " + FOCUS_END)
        lines.append("}")
        lines.append("")
    while lines and lines[-1] == "":
        lines.pop()
    return "\n".join(lines) + ("\n" if lines else "")


def _output_fallback(spec: dict, name: str) -> str:
    for rtype in spec.get("expected_resources", []):
        if rtype.startswith(("aws_", "docker_")):
            return f"{rtype}.this.id"
    return '"value"'


def _render_versions(spec: dict, focus: Focus) -> str:
    sid = spec.get("id", "")
    lines = ["terraform {", '  required_version = ">= 1.5.0"']
    if sid == "state-s3-backend":
        lines.append('  backend "s3" {')
        body = _render_node(_backend_block(), "    ", None)
        if focus.kind == "backend":
            lines.append("    " + FOCUS_START)
            lines.extend(body)
            lines.append("    " + FOCUS_END)
        else:
            lines.extend(body)
        lines.append("  }")
    elif _needs_docker(spec) and not _needs_aws(spec):
        lines.extend("  " + line for line in _provider_docker())
    elif _needs_aws(spec):
        lines.extend("  " + line for line in _provider_required())
    lines.append("}")
    return "\n".join(lines) + "\n"


def _render_provider(spec: dict) -> str:
    lines: list[str] = []
    if _needs_windows_docker(spec) or (_needs_docker(spec) and not _needs_aws(spec)):
        lines.append('provider "docker" {')
        lines.append("  host = var.docker_host")
        lines.append("}")
        lines.append("")
    if _needs_aws(spec):
        lines.append('provider "aws" {')
        lines.append("  region = var.aws_region")
        lines.append("}")
        lines.append("")
    return "\n".join(lines)


def _needs_windows_docker(spec: dict) -> bool:
    return _needs_docker(spec)


def _render_main(spec: dict, resources: dict[str, list[Res]], focus: Focus) -> str:
    chunks: list[str] = []
    provider = _render_provider(spec)
    if provider:
        chunks.append(provider.rstrip())

    sid = spec.get("id", "")
    if sid == "mod-local-module" or sid == "mod-module-for-each":
        node = _module_block(spec)
        chunks.append(
            "\n".join(
                _render_top_block(
                    "module",
                    ["this"],
                    node,
                    focus,
                    match=focus.kind == "top" and focus.block == "module",
                )
            )
        )
        return "\n\n".join(chunks) + "\n"

    if sid == "refactor-moved-block":
        chunks.append(
            'resource "aws_s3_bucket" "new" {\n  bucket = "app-assets"\n}'
        )
        chunks.append(
            "\n".join(
                _render_top_block(
                    "moved",
                    [],
                    _moved_block(),
                    focus,
                    match=focus.kind == "top" and focus.block == "moved",
                )
            )
        )
        return "\n\n".join(chunks) + "\n"

    if sid == "import-block":
        chunks.append(
            'resource "aws_s3_bucket" "this" {\n  bucket = "imported-assets"\n}'
        )
        chunks.append(
            "\n".join(
                _render_top_block(
                    "import",
                    [],
                    _import_block(),
                    focus,
                    match=focus.kind == "top" and focus.block == "import",
                )
            )
        )
        return "\n\n".join(chunks) + "\n"

    # Locals block.
    locals_node: Node | None = None
    if sid == "lang-locals-common-tags" or sid == "lang-functions-merge":
        locals_node = _locals_common_tags()
    elif sid == "state-workspaces":
        locals_node = _locals_workspace()
    if locals_node is not None:
        chunks.append(
            "\n".join(
                _render_top_block(
                    "locals",
                    [],
                    locals_node,
                    focus,
                    match=focus.kind == "top" and focus.block == "locals",
                )
            )
        )

    # Data sources.
    for dtype in _data_types(spec):
        label_name = "latest" if dtype == "aws_ami" else "this"
        match = (
            focus.kind == "top"
            and focus.block == "data"
            and (not focus.name or focus.name == label_name)
        )
        chunks.append(
            "\n".join(
                _render_top_block(
                    "data",
                    [dtype, label_name],
                    _data_node(dtype),
                    focus,
                    match=match,
                )
            )
        )

    # Resources.
    for rtype, items in resources.items():
        for res in items:
            chunks.append("\n".join(_render_res(res, focus)))

    # Wire the bucket to locals where the language exercises require it.
    if sid in ("lang-locals-common-tags", "lang-functions-merge"):
        for res in resources.get("aws_s3_bucket", []):
            res.attr("tags", "local.common_tags")
    if sid == "state-workspaces":
        for res in resources.get("aws_s3_bucket", []):
            res.attr("bucket", "local.bucket_name")

    # Re-render the resources that were modified after the first pass.
    if sid in ("lang-locals-common-tags", "lang-functions-merge", "state-workspaces"):
        chunks = [c for c in chunks if not c.startswith('resource "aws_s3_bucket"')]
        for res in resources.get("aws_s3_bucket", []):
            chunks.append("\n".join(_render_res(res, focus)))

    return "\n\n".join(chunks) + "\n"


def build_reference(spec: dict) -> dict[str, str]:
    """Build complete solution files for a spec."""
    if spec.get("reference"):
        return canonicalize_files(dict(spec["reference"]))
    focus = choose_focus(spec)
    variables = _effective_variables(spec)
    resources = _build_resources(spec)
    files = {
        "versions.tf": _render_versions(spec, focus),
        "variables.tf": _render_variables(variables, focus),
        "main.tf": _render_main(spec, resources, focus),
        "outputs.tf": _render_outputs(spec, focus),
    }
    return canonicalize_files(
        {name: text for name, text in files.items() if text.strip()}
    )


def mask_reference(
    files: dict[str, str],
    focus: Focus | dict,
    forbidden: Iterable[str] = (),
) -> dict[str, str]:
    """Replace the marked region in every file with one TODO comment."""
    if isinstance(focus, dict):
        focus = Focus(**focus)
    todo = focus.todo or "Complete this block."
    title = focus.title or "Complete the graded block"
    banned = [marker for marker in forbidden if marker]
    if any(marker in (title + "\n" + todo) for marker in banned):
        title = "Complete the graded block"
        todo = "Complete this block using the challenge requirements."
    out: dict[str, str] = {}
    for name, text in files.items():
        lines = text.split("\n")
        result: list[str] = []
        index = 0
        while index < len(lines):
            line = lines[index]
            if FOCUS_START in line:
                indent = line[: len(line) - len(line.lstrip(" "))]
                # Skip to the matching end marker.
                index += 1
                while index < len(lines) and FOCUS_END not in lines[index]:
                    index += 1
                index += 1
                result.append(f"{indent}# TODO - {title}.")
                result.append(f"{indent}# {todo}")
                continue
            if FOCUS_END in line:
                index += 1
                continue
            result.append(line)
            index += 1
        out[name] = "\n".join(result)
    return out


def render_starter(spec: dict) -> dict[str, str]:
    """Return the learner starter: complete code minus the focus region."""
    if spec.get("starter_override"):
        return dict(spec["starter_override"])
    forbidden = {
        t["check"].get("text", "")
        for t in spec.get("tests", [])
        if t.get("check", {}).get("kind") == "file_contains"
    }
    starter = mask_reference(build_reference(spec), choose_focus(spec), forbidden)
    if spec.get("id") == "intro-hcl-formatting":
        return starter
    return canonicalize_files(starter)


def level_for_spec(spec: dict) -> tuple[int, str]:
    sid = spec.get("id", "")
    difficulty = spec.get("difficulty", "Easy")
    if sid.startswith("intro-"):
        level = 0
    elif sid.startswith("lang-"):
        level = 1
    elif sid.startswith("provision-"):
        level = 2 if difficulty == "Easy" else 3
    elif sid.startswith("harden-"):
        level = 3 if difficulty in ("Easy", "Medium") else 4
    elif sid.startswith("wire-"):
        level = 4
    elif sid.startswith(("mod-", "state-", "refactor-", "import-")):
        level = 5
    elif sid.startswith("docker-"):
        level = 2 if difficulty == "Easy" else 3
    else:
        level = 2
    return level, LEVEL_NAMES[level]
