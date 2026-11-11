"""Challenge 05 — Serverless Item API (Hard)."""
from __future__ import annotations

from .. import checks as C
from ..evaluator import Challenge, TestCase
from ..hcl import has_ref, norm, object_map, unquote


def _policy_docs(cfg):
    return cfg.data_sources("aws_iam_policy_document")


def _statements(doc):
    return doc.nested("statement")


def _statement_text(statement):
    return " ".join(a.raw for a in statement.attrs) + " " + " ".join(
        a.raw for n in statement.blocks for a in n.attrs
    )


def _find_doc_statements(cfg, needle):
    for doc in _policy_docs(cfg):
        for st in _statements(doc):
            if needle in _statement_text(st):
                return doc, st
    return None, None


def t_provider(cfg):
    ok, msg = C.required_provider(cfg, "aws")
    if not ok:
        return False, msg
    provider = cfg.providers().get("aws")
    if not provider:
        return False, 'Missing provider "aws" configuration block.'
    return C.is_ref(provider, "region", "var.aws_region")


def t_table(cfg):
    table = C.first_resource(cfg, "aws_dynamodb_table")
    if not table:
        return False, "Missing aws_dynamodb_table resource."
    ok, msg = C.equals(table, "billing_mode", '"PAY_PER_REQUEST"')
    if not ok:
        return False, msg
    if norm(C.raw(table, "hash_key") or "") != '"id"':
        return False, "DynamoDB hash_key must be \"id\"."
    attrs = table.nested("attribute")
    if not attrs or norm(C.raw(attrs[0], "name") or "") != '"id' + '"':
        return False, "DynamoDB must declare an attribute named \"id\"."
    return True, "DynamoDB uses on-demand billing with hash key id."


def t_table_security(cfg):
    table = C.first_resource(cfg, "aws_dynamodb_table")
    if not table:
        return False, "Missing aws_dynamodb_table resource."
    sse = table.nested("server_side_encryption")
    if not sse or not C.is_true(sse[0], "enabled")[0]:
        return False, "DynamoDB server_side_encryption.enabled must be true."
    pitr = table.nested("point_in_time_recovery")
    if not pitr or not C.is_true(pitr[0], "enabled")[0]:
        return False, "DynamoDB point_in_time_recovery.enabled must be true."
    if C.raw(table, "deletion_protection_enabled"):
        if not C.is_true(table, "deletion_protection_enabled")[0]:
            return False, "deletion_protection_enabled must be true when set."
    return True, "DynamoDB has SSE and point-in-time recovery enabled."


def t_assume_role(cfg):
    role = C.first_resource(cfg, "aws_iam_role")
    if not role:
        return False, "Missing aws_iam_role for Lambda."
    policy = C.raw(role, "assume_role_policy") or ""
    if "data.aws_iam_policy_document." in policy:
        doc, _ = _find_doc_statements(cfg, "lambda.amazonaws.com")
        if doc:
            return True, "Assume-role policy grants lambda.amazonaws.com."
        return False, "Assume-role policy document does not trust lambda.amazonaws.com."
    if "lambda.amazonaws.com" in policy:
        return True, "Assume-role policy trusts lambda.amazonaws.com."
    return False, "assume_role_policy must trust lambda.amazonaws.com."


def t_least_privilege(cfg):
    table = C.first_resource(cfg, "aws_dynamodb_table")
    if not table:
        return False, "Missing aws_dynamodb_table resource."
    policy = C.first_resource(cfg, "aws_iam_policy")
    if not policy:
        return False, "Missing dedicated aws_iam_policy for Lambda permissions."
    raw = C.raw(policy, "policy") or ""
    if "data.aws_iam_policy_document." in raw:
        found = False
        for doc in _policy_docs(cfg):
            for st in _statements(doc):
                text = _statement_text(st)
                if "dynamodb:" in text:
                    if "aws_dynamodb_table." not in text:
                        return False, "DynamoDB statement must scope resources to the table ARN."
                    if '"*"' in text:
                        return False, "DynamoDB statement must not use wildcard actions/resources."
                    found = True
        if not found:
            return False, "No DynamoDB least-privilege statement found."
        return True, "Lambda policy is scoped to the DynamoDB table."
    if "dynamodb:" not in raw:
        return False, "IAM policy must grant specific dynamodb actions."
    if "aws_dynamodb_table." not in raw:
        return False, "IAM policy resource must reference the DynamoDB table ARN."
    if '"*"' in raw:
        return False, "IAM policy must not use wildcard actions/resources."
    return True, "Inline Lambda policy is scoped to the DynamoDB table."


def t_role_attachment(cfg):
    attach = C.first_resource(cfg, "aws_iam_role_policy_attachment")
    if not attach:
        return False, "Missing aws_iam_role_policy_attachment."
    if "aws_iam_policy." not in (C.raw(attach, "policy_arn") or ""):
        return False, "Attachment policy_arn must reference the aws_iam_policy."
    if "aws_iam_role." not in (C.raw(attach, "role") or ""):
        return False, "Attachment role must reference the aws_iam_role."
    return True, "Policy is attached to the Lambda role."


def t_lambda(cfg):
    fn = C.first_resource(cfg, "aws_lambda_function")
    if not fn:
        return False, "Missing aws_lambda_function resource."
    if "aws_iam_role." not in (C.raw(fn, "role") or ""):
        return False, "Lambda role must reference the aws_iam_role."
    ok, msg = C.is_ref(fn, "runtime", "var.lambda_runtime")
    if not ok:
        return False, msg
    ok, msg = C.is_ref(fn, "memory_size", "var.lambda_memory")
    if not ok:
        return False, msg
    handler = C.raw(fn, "handler") or ""
    if "lambda_handler" not in handler:
        return False, f"handler must be handler.lambda_handler, found {handler!r}."
    if not C.present(fn, "filename") and not C.present(fn, "image_uri"):
        return False, "Lambda requires a filename or image_uri."
    return True, "Lambda is wired to role, runtime and memory variables."


def t_lambda_timeout(cfg):
    fn = C.first_resource(cfg, "aws_lambda_function")
    if not fn:
        return False, "Missing aws_lambda_function resource."
    timeout = C.raw(fn, "timeout")
    if timeout is None:
        return True, "timeout omitted (defaults to 3s)."
    kind, val = C.value(fn, "timeout")
    if kind == "number" and int(val) <= 10:
        return True, f"Lambda timeout is {val}s (<= 10)."
    if kind == "number":
        return False, f"Lambda timeout {val}s exceeds the 10s cap."
    return False, "Lambda timeout must be a literal number <= 10."


def t_lambda_env(cfg):
    fn = C.first_resource(cfg, "aws_lambda_function")
    if not fn:
        return False, "Missing aws_lambda_function resource."
    env = fn.nested("environment")
    if not env:
        return False, "Lambda is missing an environment block."
    variables = object_map(env[0].attr("variables")) or {}
    if "TABLE_NAME" not in variables:
        return False, "Lambda environment must expose TABLE_NAME."
    if "aws_dynamodb_table." not in variables["TABLE_NAME"]:
        return False, "TABLE_NAME must reference the DynamoDB table."
    return True, "Lambda receives TABLE_NAME from the table resource."


def t_concurrency(cfg):
    fn = C.first_resource(cfg, "aws_lambda_function")
    if not fn:
        return False, "Missing aws_lambda_function resource."
    raw = C.raw(fn, "reserved_concurrent_executions")
    if raw is None:
        return False, "Lambda must cap concurrency with reserved_concurrent_executions (<= 5)."
    kind, val = C.value(fn, "reserved_concurrent_executions")
    if kind == "number" and 0 < int(val) <= 5:
        return True, f"reserved_concurrent_executions = {val}."
    return False, f"reserved_concurrent_executions must be between 1 and 5, found {raw!r}."


def t_http_api(cfg):
    api = C.first_resource(cfg, "aws_apigatewayv2_api")
    if not api:
        return False, "Missing aws_apigatewayv2_api resource."
    if norm(C.raw(api, "protocol_type") or "") != '"HTTP"':
        return False, "API Gateway protocol_type must be HTTP."
    return True, "HTTP API Gateway is provisioned."


def t_integration(cfg):
    integ = C.first_resource(cfg, "aws_apigatewayv2_integration")
    if not integ:
        return False, "Missing aws_apigatewayv2_integration resource."
    if norm(C.raw(integ, "integration_type") or "") != '"AWS_PROXY"':
        return False, "Integration type must be AWS_PROXY."
    uri = C.raw(integ, "integration_uri") or ""
    if "aws_lambda_function." not in uri or "invoke_arn" not in uri:
        return False, "integration_uri must use the Lambda invoke_arn."
    if norm(C.raw(integ, "payload_format_version") or "") != '"2.0"':
        return False, "payload_format_version must be 2.0."
    if norm(C.raw(integ, "integration_method") or "") not in ('"POST"', ""):
        return False, "integration_method should be POST for AWS_PROXY."
    return True, "API Gateway integrates with Lambda via AWS_PROXY."


def t_route_stage(cfg):
    route = C.first_resource(cfg, "aws_apigatewayv2_route")
    if not route:
        return False, "Missing aws_apigatewayv2_route resource."
    if "GET" not in (C.raw(route, "route_key") or ""):
        return False, "Route key must include GET /items."
    if "aws_apigatewayv2_integration." not in (C.raw(route, "target") or ""):
        return False, "Route target must reference the integration."
    stage = C.first_resource(cfg, "aws_apigatewayv2_stage")
    if not stage:
        return False, "Missing aws_apigatewayv2_stage resource."
    if not C.is_true(stage, "auto_deploy")[0]:
        return False, "Stage must set auto_deploy = true."
    ok, msg = C.is_ref(stage, "name", "var.api_stage")
    if not ok:
        return False, msg
    return True, "GET route is wired and the stage auto-deploys."


def t_permission(cfg):
    perm = C.first_resource(cfg, "aws_lambda_permission")
    if not perm:
        return False, "Missing aws_lambda_permission for API Gateway."
    if "apigateway" not in (C.raw(perm, "principal") or ""):
        return False, "Lambda permission principal must be apigateway.amazonaws.com."
    if "InvokeFunction" not in (C.raw(perm, "action") or ""):
        return False, "Lambda permission action must be lambda:InvokeFunction."
    if "aws_lambda_function." not in (C.raw(perm, "function_name") or ""):
        return False, "Lambda permission must reference the function."
    return True, "API Gateway is allowed to invoke the Lambda."


def t_outputs(cfg):
    for name, ref in (
        ("api_endpoint", "aws_apigatewayv2_"),
        ("lambda_name", "aws_lambda_function."),
        ("table_name", "aws_dynamodb_table."),
    ):
        ok, msg = C.output_ok(cfg, name)
        if not ok:
            return False, msg
        out = C.get_output(cfg, name)
        if out and ref not in (C.raw(out, "value") or ""):
            return False, f"Output {name} must reference {ref}"
    return True, "API, Lambda and table outputs are exposed."


def t_tags(cfg):
    for rtype in ("aws_dynamodb_table", "aws_lambda_function", "aws_iam_role"):
        res = C.first_resource(cfg, rtype)
        if not res:
            return False, f"Missing {rtype}."
        merged = C.effective_tags(cfg, res)
        for key in ("Project", "Environment", "ManagedBy"):
            if key not in merged:
                return False, f"{rtype} is missing tag '{key}'."
    return True, "Serverless resources carry the standard tags."


def t_usage(cfg):
    used = cfg.referenced_variables()
    missing = [
        n
        for n in ("table_name", "lambda_runtime", "lambda_memory", "api_stage")
        if n not in used
    ]
    if missing:
        return False, "Variables declared but not referenced: " + ", ".join(missing)
    return True, "Core variables are wired into resources."


CHALLENGE = Challenge(
    id="serverless-item-api",
    number=5,
    title="Serverless Item API",
    difficulty="Hard",
    points=300,
    tags=["aws", "lambda", "dynamodb", "api-gateway", "iam"],
    scenario=(
        "Ship a serverless CRUD endpoint with least-privilege IAM. Provision a DynamoDB "
        "table with encryption and point-in-time recovery, a Python Lambda that receives the "
        "table name through its environment, and an HTTP API Gateway route that proxies GET "
        "/items to the function. Cap concurrency so a runaway loop cannot burn the free tier."
    ),
    constraints=[
        "Provider: AWS with region from var.aws_region.",
        "DynamoDB: PAY_PER_REQUEST billing, hash key id (type S), SSE enabled, PITR enabled.",
        "Lambda execution role must trust lambda.amazonaws.com.",
        "A dedicated aws_iam_policy must grant only the DynamoDB actions needed, scoped to the table ARN (no \"*\").",
        "Attach the policy to the role with aws_iam_role_policy_attachment.",
        "Lambda: runtime and memory from variables, handler handler.lambda_handler, timeout <= 10s, reserved_concurrent_executions between 1 and 5.",
        "Lambda environment must expose TABLE_NAME referencing the table.",
        "HTTP API Gateway (protocol_type HTTP) with AWS_PROXY integration to the Lambda invoke_arn and payload_format_version 2.0.",
        "Route key GET /items, stage auto_deploy = true and name from var.api_stage.",
        "Grant API Gateway lambda:InvokeFunction through aws_lambda_permission.",
        "Tag DynamoDB, Lambda and the IAM role with Project, Environment, ManagedBy = \"terraform\".",
        "Outputs: api_endpoint, lambda_name, table_name.",
    ],
    variables=[
        {"name": "table_name", "type": "string", "default": "items"},
        {"name": "lambda_runtime", "type": "string", "default": "python3.12"},
        {"name": "lambda_memory", "type": "number", "default": 128, "validation": True},
        {"name": "api_stage", "type": "string", "default": "prod"},
        {"name": "aws_region", "type": "string", "default": "us-east-1"},
        {"name": "project_name", "type": "string", "default": "terraform-practice"},
        {"name": "environment", "type": "string", "default": "dev", "validation": True},
    ],
    expected_resources=[
        "aws_dynamodb_table",
        "aws_iam_role",
        "aws_iam_policy",
        "aws_iam_role_policy_attachment",
        "aws_lambda_function",
        "aws_lambda_permission",
        "aws_apigatewayv2_api",
        "aws_apigatewayv2_integration",
        "aws_apigatewayv2_route",
        "aws_apigatewayv2_stage",
    ],
    expected_outputs=["api_endpoint", "lambda_name", "table_name"],
    starter={
        "versions.tf": "# versions.tf\n# TODO: terraform block + AWS provider.\n",
        "variables.tf": "# variables.tf\n# TODO: table_name, lambda_runtime, lambda_memory, api_stage, tags.\n",
        "main.tf": "# main.tf\n# TODO: DynamoDB, IAM role/policy, Lambda, API Gateway.\n",
        "outputs.tf": "# outputs.tf\n# TODO: api_endpoint, lambda_name, table_name.\n",
    },
    allowlist=[
        "aws_dynamodb_table",
        "aws_iam_role",
        "aws_iam_policy",
        "aws_iam_role_policy_attachment",
        "aws_lambda_function",
        "aws_lambda_permission",
        "aws_apigatewayv2_api",
        "aws_apigatewayv2_integration",
        "aws_apigatewayv2_route",
        "aws_apigatewayv2_stage",
        "aws_cloudwatch_log_group",
    ],
    data_allowlist=[
        "aws_iam_policy_document",
        "aws_region",
        "aws_caller_identity",
        "archive_file",
    ],
    tests=[
        TestCase("lambda-provider", "AWS provider + region variable", "Providers", 4, t_provider),
        TestCase("lambda-table", "DynamoDB on-demand + hash key", "Resources", 6, t_table),
        TestCase("lambda-table-sec", "DynamoDB SSE + PITR", "Security", 7, t_table_security),
        TestCase("lambda-assume", "Lambda trust policy", "Security", 6, t_assume_role),
        TestCase("lambda-least-priv", "Least-privilege DynamoDB policy", "Security", 9, t_least_privilege),
        TestCase("lambda-attach", "Policy attached to role", "Resources", 5, t_role_attachment),
        TestCase("lambda-fn", "Lambda wiring", "Resources", 8, t_lambda),
        TestCase("lambda-timeout", "Lambda timeout <= 10s", "Lifecycle", 5, t_lambda_timeout),
        TestCase("lambda-env", "TABLE_NAME environment injection", "Resources", 6, t_lambda_env),
        TestCase("lambda-concurrency", "Concurrency capped 1–5", "Security", 7, t_concurrency),
        TestCase("lambda-api", "HTTP API Gateway", "Resources", 5, t_http_api),
        TestCase("lambda-integration", "AWS_PROXY integration", "Resources", 7, t_integration),
        TestCase("lambda-route", "Route + auto-deploy stage", "Resources", 7, t_route_stage),
        TestCase("lambda-permission", "API Gateway invoke permission", "Security", 6, t_permission),
        TestCase("lambda-outputs", "Required outputs exposed", "Outputs", 5, t_outputs),
        TestCase("lambda-tags", "Serverless resources tagged", "Lifecycle", 5, t_tags),
        TestCase("lambda-usage", "Variables wired into resources", "Modularity", 4, t_usage),
    ],
)
