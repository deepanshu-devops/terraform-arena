"""Declarative challenge compiler.

A challenge spec is a plain dict. Its tests are described as small
``{"kind": ..., ...}`` objects that the dispatcher below interprets. This is
what makes it possible to ship 100+ scenarios without 100 bespoke modules.
"""
from __future__ import annotations

import re
from typing import Any

from . import checks as C
from .evaluator import Challenge, TestCase
from .hcl import Block, Config, has_ref, literal, norm, unquote


# ---------------------------------------------------------------------------
# numeric helpers
# ---------------------------------------------------------------------------
def _number(cfg: Config, block: Block | None, attr: str):
    if not block:
        return None
    kind, val = C.value(block, attr)
    if kind == "number":
        return val
    raw = C.raw(block, attr) or ""
    m = re.search(r"\bvar\.([A-Za-z_][A-Za-z0-9_-]*)", raw)
    if m:
        var = cfg.variables().get(m.group(1))
        kind, val = C.var_default(var)
        if kind == "number":
            return val
    return None


def _num_check(cfg, check, comparator) -> tuple[bool, str]:
    resource = check["resource"]
    attr = check["attr"]
    target = check["value"]
    block = C.first_resource(cfg, resource)
    if not block:
        return False, f"Missing resource '{resource}'."
    val = _number(cfg, block, attr)
    if val is None:
        return False, f"Could not resolve numeric value for {resource}.{attr}."
    if comparator(val, target):
        return True, f"{resource}.{attr} = {val}."
    return False, f"{resource}.{attr} must be {'<=' if comparator.__name__ == 'le' else '>='} {target}, found {val}."


def le(a, b):
    return a <= b


def ge(a, b):
    return a >= b


def _walk(block: Block | None, path: list[str]) -> Block | None:
    cur = block
    for part in path:
        if cur is None:
            return None
        nested = cur.nested(part)
        if not nested:
            return None
        cur = nested[0]
    return cur


# ---------------------------------------------------------------------------
# Dispatcher
# ---------------------------------------------------------------------------
def run_check(cfg: Config, check: dict[str, Any]) -> tuple[bool, str]:
    kind = check.get("kind")

    if kind == "resource_exists":
        rtype = check["type"]
        count = len(cfg.resources(rtype))
        return (True, f"Found {rtype}.") if count else (False, f"Missing resource '{rtype}'.")

    if kind == "resource_count":
        rtype = check["type"]
        n = len(cfg.resources(rtype))
        lo = check.get("min", 1)
        hi = check.get("max")
        if n < lo:
            return False, f"Expected at least {lo} '{rtype}', found {n}."
        if hi is not None and n > hi:
            return False, f"Expected at most {hi} '{rtype}', found {n}."
        return True, f"Found {n} '{rtype}'."

    if kind == "attr_equals":
        return C.equals(C.first_resource(cfg, check["resource"]), check["attr"], check["value"])

    if kind == "attr_ref":
        return C.is_ref(C.first_resource(cfg, check["resource"]), check["attr"], check["ref"])

    if kind == "attr_present":
        block = C.first_resource(cfg, check["resource"])
        return (
            (True, f"{check['resource']}.{check['attr']} is set.")
            if C.present(block, check["attr"])
            else (False, f"Missing {check['resource']}.{check['attr']}.")
        )

    if kind == "attr_absent":
        block = C.first_resource(cfg, check["resource"])
        return (
            (False, f"{check['resource']}.{check['attr']} must not be set.")
            if C.present(block, check["attr"])
            else (True, f"{check['resource']}.{check['attr']} is absent.")
        )

    if kind == "attr_contains":
        block = C.first_resource(cfg, check["resource"])
        raw = (C.raw(block, check["attr"]) or "") if block else ""
        if check["text"] in raw:
            return True, f"{check['resource']}.{check['attr']} contains {check['text']!r}."
        return False, f"{check['resource']}.{check['attr']} must contain {check['text']!r}."

    if kind == "attr_number_max":
        return _num_check(cfg, check, le)

    if kind == "attr_number_min":
        return _num_check(cfg, check, ge)

    if kind == "nested_equals":
        return C.nested_equals(
            C.first_resource(cfg, check["resource"]),
            check["block"],
            check["attr"],
            check["value"],
        )

    if kind == "nested_present":
        return C.nested_present(
            C.first_resource(cfg, check["resource"]),
            check["block"],
            check.get("attr"),
        )

    if kind == "nested_ref":
        block = C.first_resource(cfg, check["resource"])
        if not block:
            return False, f"Missing resource '{check['resource']}'."
        nested = block.nested(check["block"])
        if not nested:
            return False, f"Missing nested block '{check['block']}'."
        return C.is_ref(nested[0], check["attr"], check["ref"])

    if kind == "nested_count_min":
        block = C.first_resource(cfg, check["resource"])
        if not block:
            return False, f"Missing resource '{check['resource']}'."
        n = len(block.nested(check["block"]))
        if n >= check["min"]:
            return True, f"{check['resource']} has {n} '{check['block']}' block(s)."
        return False, f"Expected >= {check['min']} '{check['block']}' blocks, found {n}."

    if kind == "nested_path_present":
        block = C.first_resource(cfg, check["resource"])
        if not block:
            return False, f"Missing resource '{check['resource']}'."
        if _walk(block, check["path"]) is None:
            return False, f"Missing nested path: {'.'.join(check['path'])}."
        return True, f"Nested path {'.'.join(check['path'])} is present."

    if kind == "nested_path":
        block = C.first_resource(cfg, check["resource"])
        if not block:
            return False, f"Missing resource '{check['resource']}'."
        node = _walk(block, check["path"])
        if node is None:
            return False, f"Missing nested path: {'.'.join(check['path'])}."
        return C.equals(node, check["attr"], check["value"])

    if kind == "nested_path_max":
        block = C.first_resource(cfg, check["resource"])
        if not block:
            return False, f"Missing resource '{check['resource']}'."
        node = _walk(block, check["path"])
        if node is None:
            return False, f"Missing nested path: {'.'.join(check['path'])}."
        val = _number(cfg, node, check["attr"])
        if val is None:
            return False, f"Could not resolve numeric {'.'.join(check['path'])}.{check['attr']}."
        if val <= check["value"]:
            return True, f"{'.'.join(check['path'])}.{check['attr']} = {val}."
        return False, f"{'.'.join(check['path'])}.{check['attr']} must be <= {check['value']}, found {val}."

    if kind == "tagged":
        resources = check["resources"]
        required = check["tags"]
        issues = []
        for rtype in resources:
            block = C.first_resource(cfg, rtype)
            if not block:
                issues.append(f"Missing {rtype}")
                continue
            merged = C.effective_tags(cfg, block)
            for key, expected in required.items():
                if key not in merged:
                    issues.append(f"{rtype}: missing tag {key}")
                elif norm(merged[key]) != norm(expected):
                    issues.append(f"{rtype}: tag {key} expected {expected!r}, found {merged[key]!r}")
        if issues:
            return False, "; ".join(issues[:6])
        return True, "Required tags are present."

    if kind == "has_tag":
        return C.tag_value(cfg, check["resource"], check["key"])

    if kind == "all_tagged":
        return C.all_resources_tagged(cfg, check["tags"])

    if kind == "required_provider":
        return C.required_provider(cfg, check["name"])

    if kind == "provider_ref":
        return C.provider_attr_ref(cfg, check["provider"], check["attr"], check["ref"])

    if kind == "var_defined":
        return C.variable_defined(
            cfg,
            check["name"],
            expected_type=check.get("type"),
            expected_default=check.get("default") if check.get("default") is not None else None,
            require_validation=check.get("validation", False),
        )

    if kind == "var_validation_contains":
        var = C.get_var(cfg, check["name"])
        if not var:
            return False, f"Variable '{check['name']}' is not defined."
        text = C.validation_text(var)
        if not text:
            return False, f"Variable '{check['name']}' has no validation."
        missing = [v for v in check["values"] if str(v) not in text]
        if missing:
            return False, f"Validation for '{check['name']}' is missing: {', '.join(map(str, missing))}."
        return True, f"Validation for '{check['name']}' covers the required values."

    if kind == "output_exists":
        return C.output_ok(cfg, check["name"])

    if kind == "output_attr":
        out = C.get_output(cfg, check["name"])
        if not out:
            return False, f"Output '{check['name']}' is not defined."
        if check.get("equals") is not None:
            return C.equals(out, check["attr"], check["equals"])
        if C.present(out, check["attr"]):
            return True, f"Output '{check['name']}' has {check['attr']}."
        return False, f"Output '{check['name']}' must set {check['attr']}."

    if kind == "var_attr":
        var = C.get_var(cfg, check["name"])
        if not var:
            return False, f"Variable '{check['name']}' is not defined."
        if check.get("equals") is not None:
            return C.equals(var, check["attr"], check["equals"])
        if C.present(var, check["attr"]):
            return True, f"Variable '{check['name']}' has {check['attr']}."
        return False, f"Variable '{check['name']}' must set {check['attr']}."

    if kind == "output_ref":
        ok, msg = C.output_ok(cfg, check["name"])
        if not ok:
            return False, msg
        out = C.get_output(cfg, check["name"])
        value = C.raw(out, "value") or ""
        if check["ref"] in value:
            return True, f"Output {check['name']} references {check['ref']}."
        return False, f"Output {check['name']} must reference {check['ref']}."

    if kind == "data_exists":
        dtype = check["type"]
        return (
            (True, f"Found data.{dtype}.")
            if cfg.data_sources(dtype)
            else (False, f"Missing data '{dtype}'.")
        )

    if kind == "module_exists":
        modules = cfg.top("module")
        needle = check.get("source_contains", "")
        for module in modules:
            src = C.raw(module, "source") or ""
            if needle in src:
                return True, f"Module source contains {needle!r}."
        if modules and not needle:
            return True, f"Found {len(modules)} module block(s)."
        return False, f"No module block with source containing {needle!r}."

    if kind == "file_contains":
        needle = check["text"]
        for fname, src in cfg.files.items():
            if needle in src:
                return True, f"{fname} contains {needle!r}."
        return False, f"No file contains {needle!r}."

    if kind == "count_or_foreach":
        block = C.first_resource(cfg, check["resource"])
        if not block:
            return False, f"Missing resource '{check['resource']}'."
        if C.present(block, "count") or C.present(block, "for_each"):
            return True, f"{check['resource']} uses count/for_each."
        return False, f"{check['resource']} must use count or for_each."

    if kind == "lifecycle_prevent_destroy":
        block = C.first_resource(cfg, check["resource"])
        if not block:
            return False, f"Missing resource '{check['resource']}'."
        lifecycles = block.nested("lifecycle")
        if not lifecycles:
            return False, "Missing lifecycle block."
        return C.is_true(lifecycles[0], "prevent_destroy")

    if kind == "depends_on_present":
        block = C.first_resource(cfg, check["resource"])
        if not block:
            return False, f"Missing resource '{check['resource']}'."
        if C.present(block, "depends_on"):
            return True, "depends_on is present."
        return False, "depends_on is required."

    if kind == "no_hardcoded_creds":
        return C.no_hardcoded_credentials(cfg)

    if kind == "no_public_acl":
        return C.no_public_acl(cfg)

    if kind == "no_open_ssh":
        for sg in cfg.resources("aws_security_group"):
            for rule in sg.nested("ingress"):
                frm = C.raw(rule, "from_port") or ""
                to = C.raw(rule, "to_port") or ""
                cidrs = C.raw(rule, "cidr_blocks") or ""
                if norm(frm) == "22" and norm(to) == "22" and "0.0.0.0/0" in cidrs:
                    return False, "SSH/22 must not be open to 0.0.0.0/0."
        return True, "No world-open SSH ingress."

    if kind == "no_wildcard_iam":
        for fname, src in cfg.files.items():
            if re.search(r'("Action"\s*:\s*"\*"|Action\s*=\s*"?\*"?)', src):
                return False, f"{fname}: wildcard IAM action detected."
        return True, "No wildcard IAM actions."

    if kind == "expr_contains":
        block = C.first_resource(cfg, check["resource"])
        raw = (C.raw(block, check["attr"]) or "") if block else ""
        if check["text"] in raw:
            return True, f"{check['resource']}.{check['attr']} contains {check['text']!r}."
        return False, f"{check['resource']}.{check['attr']} must contain {check['text']!r}."

    if kind == "formatting_clean":
        issues = C.formatting_issues(cfg.files)
        if not issues:
            return True, "Formatting matches Terraform style."
        return False, "; ".join(issues[:4])

    return False, f"Unknown check kind: {kind!r}"


# ---------------------------------------------------------------------------
# Spec -> Challenge
# ---------------------------------------------------------------------------
def _test_from_dict(spec: dict) -> TestCase:
    check = spec["check"]
    return TestCase(
        id=spec["id"],
        title=spec["title"],
        category=spec.get("category", "Resources"),
        weight=spec.get("weight", 5),
        required=spec.get("required", True),
        hint=spec.get("hint", ""),
        fn=lambda cfg, c=check: run_check(cfg, c),
    )


def build_challenge(spec: dict, number: int) -> Challenge:
    tests = [_test_from_dict(t) for t in spec["tests"]]
    return Challenge(
        id=spec["id"],
        number=number,
        title=spec["title"],
        difficulty=spec.get("difficulty", "Easy"),
        points=spec.get("points", 50),
        tags=spec.get("tags", []),
        scenario=spec.get("scenario", ""),
        constraints=spec.get("constraints", []),
        variables=spec.get("variables", []),
        expected_resources=spec.get("expected_resources", []),
        expected_outputs=spec.get("expected_outputs", []),
        starter=spec.get("starter", {}),
        tests=tests,
        allowlist=spec.get("allowlist", []),
        data_allowlist=spec.get("data_allowlist", []),
        apply_sandbox=spec.get("apply_sandbox", False),
        level=spec.get("level", 0),
        level_name=spec.get("level_name", ""),
        focus=spec.get("focus", {}),
        reference=spec.get("reference", {}),
    )
