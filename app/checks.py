"""Reusable assertions used by challenge test-suites.

Every check returns a ``(passed: bool, detail: str)`` tuple.
"""
from __future__ import annotations

import re
from typing import Optional

from .hcl import (
    Attr,
    Block,
    Config,
    has_ref,
    literal,
    norm,
    object_map,
    ref_vars,
    unquote,
)


def ok(msg: str = "Passed.") -> tuple[bool, str]:
    return True, msg


def fail(msg: str) -> tuple[bool, str]:
    return False, msg


def need(cond: bool, good: str, bad: str) -> tuple[bool, str]:
    return ok(good) if cond else fail(bad)


# ---------------------------------------------------------------------------
# Resource / block helpers
# ---------------------------------------------------------------------------
def first_resource(cfg: Config, rtype: str) -> Optional[Block]:
    rs = cfg.resources(rtype)
    return rs[0] if rs else None


def raw(block: Optional[Block], name: str) -> Optional[str]:
    if not block:
        return None
    attr = block.attr(name)
    return norm(attr.raw) if attr else None


def present(block: Optional[Block], name: str) -> bool:
    return bool(block and block.attr(name))


def value(block: Optional[Block], name: str):
    r = raw(block, name)
    return literal(r) if r is not None else (None, None)


def equals(block: Optional[Block], name: str, expected: str) -> tuple[bool, str]:
    r = raw(block, name)
    if r is None:
        return fail(f"Missing attribute '{name}'.")
    if norm(r) == norm(expected):
        return ok(f"{name} = {r}")
    # tolerate quoted-vs-unquoted string comparison
    if unquote(r) is not None and unquote(expected) is not None:
        if unquote(r) == unquote(expected):
            return ok(f"{name} = {r}")
    return fail(f"Expected {name} = {expected!r}, found {r!r}.")


def is_ref(block: Optional[Block], name: str, ref: str) -> tuple[bool, str]:
    r = raw(block, name)
    if r is None:
        return fail(f"Missing attribute '{name}'.")
    if norm(r) == norm(ref) or has_ref(r, ref):
        return ok(f"{name} references {ref}.")
    return fail(f"Expected {name} to reference {ref!r}, found {r!r}.")


def is_true(block: Optional[Block], name: str) -> tuple[bool, str]:
    return equals(block, name, "true")


def is_false(block: Optional[Block], name: str) -> tuple[bool, str]:
    return equals(block, name, "false")


def nested_equals(
    block: Optional[Block],
    nested_type: str,
    attr: str,
    expected: str,
) -> tuple[bool, str]:
    if not block:
        return fail("Resource block not found.")
    nested = block.nested(nested_type)
    if not nested:
        return fail(f"Missing nested block '{nested_type}'.")
    for n in nested:
        got = raw(n, attr)
        if got is not None and norm(got) == norm(expected):
            return ok(f"{nested_type}.{attr} = {expected}")
    got = raw(nested[0], attr)
    return fail(f"Expected {nested_type}.{attr} = {expected!r}, found {got!r}.")


def nested_present(block: Optional[Block], nested_type: str, attr: Optional[str] = None):
    if not block:
        return fail("Resource block not found.")
    nested = block.nested(nested_type)
    if not nested:
        return fail(f"Missing nested block '{nested_type}'.")
    if attr is not None and not any(n.attr(attr) for n in nested):
        return fail(f"Nested block '{nested_type}' is missing '{attr}'.")
    return ok(f"Found nested block '{nested_type}'.")


# ---------------------------------------------------------------------------
# Tags
# ---------------------------------------------------------------------------
def _object_from_tokens(tokens) -> dict[str, str]:
    return object_map(Attr(name="tags", raw="", tokens=tokens, line=0)) or {}


def resolve_tag_expr(cfg: Config, attr: Optional[Attr], depth: int = 0) -> dict[str, str]:
    """Resolve a tags expression, following ``local.*`` and ``merge(...)``.

    Learners are encouraged to keep common tags in locals and compose them
    with merge(), so the grader must understand those expressions instead of
    only inline object literals.
    """
    if attr is None or depth > 6:
        return {}

    direct = object_map(attr)
    if direct is not None:
        return direct

    merged: dict[str, str] = {}
    # local.<name> references anywhere in the expression
    for match in re.finditer(r"\blocal\.([A-Za-z_][\w-]*)", attr.raw):
        local_attr = cfg.locals_map().get(match.group(1))
        if local_attr is not None:
            merged.update(resolve_tag_expr(cfg, local_attr, depth + 1))

    # every top-level { ... } object literal (e.g. merge(local.tags, {...}))
    stack: list[object] = []
    start: Optional[int] = None
    for index, token in enumerate(attr.tokens):
        if token.type == "LBRACE":
            if not stack:
                start = index
            stack.append(token)
        elif token.type == "RBRACE" and stack:
            stack.pop()
            if not stack and start is not None:
                merged.update(_object_from_tokens(attr.tokens[start : index + 1]))
                start = None
    return merged


def tags_map(block: Optional[Block], cfg: Optional[Config] = None) -> dict[str, str]:
    if not block:
        return {}
    attr = block.attr("tags")
    if attr is None:
        return {}
    if cfg is not None:
        return resolve_tag_expr(cfg, attr)
    return object_map(attr) or {}


def provider_default_tags(cfg: Config) -> dict[str, str]:
    for provider in cfg.providers().values():
        for dt in provider.nested("default_tags"):
            m = object_map(dt.attr("tags"))
            if m:
                return m
    return {}


def effective_tags(cfg: Config, block: Block) -> dict[str, str]:
    merged = dict(provider_default_tags(cfg))
    merged.update(tags_map(block, cfg))
    return merged


def all_resources_tagged(
    cfg: Config, required: dict[str, str]
) -> tuple[bool, str]:
    defaults = provider_default_tags(cfg)
    issues: list[str] = []
    for res in cfg.resources():
        rtype = res.labels[0] if res.labels else "resource"
        merged = dict(defaults)
        merged.update(tags_map(res, cfg))
        for key, expected in required.items():
            if key not in merged:
                issues.append(f"{rtype}: missing tag '{key}'")
            elif norm(merged[key]) != norm(expected):
                issues.append(
                    f"{rtype}: tag '{key}' expected {expected!r}, found {merged[key]!r}"
                )
    if issues:
        return fail("; ".join(issues[:6]) + (" ..." if len(issues) > 6 else ""))
    return ok(f"All {len(cfg.resources())} resources carry required tags.")


def tag_value(cfg: Config, rtype: str, key: str) -> tuple[bool, str]:
    res = first_resource(cfg, rtype)
    if not res:
        return fail(f"Missing resource 'aws_{rtype}'.")
    merged = effective_tags(cfg, res)
    if key not in merged:
        return fail(f"Missing tag '{key}' on {rtype}.")
    return ok(f"{key} = {merged[key]}")


# ---------------------------------------------------------------------------
# Variables / outputs / providers
# ---------------------------------------------------------------------------
def get_var(cfg: Config, name: str) -> Optional[Block]:
    return cfg.variables().get(name)


def var_type(var: Optional[Block]) -> Optional[str]:
    return raw(var, "type")


def var_default(var: Optional[Block]):
    if not var:
        return (None, None)
    attr = var.attr("default")
    return literal(attr.raw) if attr else (None, None)


def var_validations(var: Optional[Block]) -> list[str]:
    if not var:
        return []
    out = []
    for v in var.nested("validation"):
        cond = v.attr("condition")
        if cond:
            out.append(norm(cond.raw))
    return out


def variable_defined(
    cfg: Config,
    name: str,
    expected_type: Optional[str] = None,
    expected_default=None,
    require_validation: bool = False,
) -> tuple[bool, str]:
    var = get_var(cfg, name)
    if not var:
        return fail(f"Variable '{name}' is not defined.")
    if expected_type is not None:
        got = var_type(var)
        if norm(got or "") != norm(expected_type):
            return fail(
                f"Variable '{name}' type expected {expected_type!r}, found {got!r}."
            )
    if expected_default is not None:
        _, got = var_default(var)
        if got != expected_default:
            return fail(
                f"Variable '{name}' default expected {expected_default!r}, found {got!r}."
            )
    if require_validation and not var.nested("validation"):
        return fail(f"Variable '{name}' is missing a validation block.")
    return ok(f"Variable '{name}' is compliant.")


def validation_text(var: Optional[Block]) -> str:
    return " ".join(var_validations(var))


def get_output(cfg: Config, name: str) -> Optional[Block]:
    return cfg.outputs().get(name)


def output_ok(cfg: Config, name: str) -> tuple[bool, str]:
    out = get_output(cfg, name)
    if not out:
        return fail(f"Output '{name}' is not defined.")
    if not out.attr("value"):
        return fail(f"Output '{name}' is missing a value.")
    return ok(f"Output '{name}' is defined.")


def required_provider(cfg: Config, name: str) -> tuple[bool, str]:
    providers = cfg.required_providers()
    if name not in providers:
        return fail(f"Provider '{name}' is not declared in required_providers.")
    return ok(f"Provider '{name}' declared: {providers[name]}")


def provider_attr_ref(cfg: Config, provider: str, attr: str, ref: str):
    block = cfg.providers().get(provider)
    if not block:
        return fail(f"Missing provider '{provider}'.")
    return is_ref(block, attr, ref)


# ---------------------------------------------------------------------------
# Security helpers
# ---------------------------------------------------------------------------
def no_hardcoded_credentials(cfg: Config) -> tuple[bool, str]:
    import re

    bad: list[str] = []
    for provider in cfg.providers().values():
        for key in ("access_key", "secret_key", "token"):
            attr = provider.attr(key)
            if attr:
                kind, val = literal(attr.raw)
                if kind == "string" and val:
                    bad.append(f"provider.{key} is hardcoded")
    for fname, src in cfg.files.items():
        if re.search(r"AKIA[0-9A-Z]{16}", src):
            bad.append(f"{fname}: AWS access key literal detected")
        if re.search(r"aws_secret_access_key\s*=\s*\"[^\"]{20,}\"", src):
            bad.append(f"{fname}: AWS secret key literal detected")
    if bad:
        return fail("; ".join(bad))
    return ok("No hardcoded credentials detected.")


def no_public_acl(cfg: Config) -> tuple[bool, str]:
    bad: list[str] = []
    for res in cfg.resources():
        acl = raw(res, "acl")
        if acl and unquote(acl) in ("public-read", "public-read-write", "authenticated-read"):
            bad.append(f"{res.labels[0]}: acl={acl}")
    if bad:
        return fail("; ".join(bad))
    return ok("No public ACLs detected.")


def no_dangerous_provisioners(cfg: Config) -> tuple[bool, str]:
    bad: list[str] = []
    for res in cfg.resources():
        for prov in res.nested("provisioner"):
            name = prov.labels[0] if prov.labels else "?"
            if name in ("local-exec", "remote-exec"):
                bad.append(f"{res.labels[0]} uses provisioner '{name}'")
    if bad:
        return fail("; ".join(bad))
    return ok("No shell provisioners detected.")


def referenced_variables(cfg: Config) -> set[str]:
    return cfg.referenced_variables()


def var_is_used(cfg: Config, name: str) -> tuple[bool, str]:
    used = cfg.referenced_variables()
    if name in used:
        return ok(f"var.{name} is referenced.")
    return fail(f"Variable '{name}' is declared but never referenced.")


# ---------------------------------------------------------------------------
# Formatting
# ---------------------------------------------------------------------------
def formatting_issues(files: dict[str, str]) -> list[str]:
    issues: list[str] = []
    for fname, src in files.items():
        lines = src.split("\n")
        if src and not src.endswith("\n"):
            issues.append(f"{fname}: file does not end with a newline")
        blank_run = 0
        for idx, line in enumerate(lines, 1):
            if "\t" in line:
                issues.append(f"{fname}:{idx}: tab character (use 2 spaces)")
            if line.rstrip() != line:
                issues.append(f"{fname}:{idx}: trailing whitespace")
            if len(line) > 140:
                issues.append(f"{fname}:{idx}: line exceeds 140 characters")
            stripped = line.lstrip(" ")
            indent = len(line) - len(stripped)
            if stripped and indent % 2 != 0:
                issues.append(f"{fname}:{idx}: indentation is not a multiple of 2")
            if not stripped:
                blank_run += 1
                if blank_run > 1:
                    issues.append(f"{fname}:{idx}: multiple consecutive blank lines")
            else:
                blank_run = 0
        if "\r\n" in src:
            issues.append(f"{fname}: CRLF line endings (terraform fmt expects LF)")
    # de-duplicate, cap noise
    seen: list[str] = []
    for i in issues:
        if i not in seen:
            seen.append(i)
    return seen


def grade_from_score(score: int) -> str:
    if score >= 95:
        return "A"
    if score >= 85:
        return "B"
    if score >= 70:
        return "C"
    if score >= 60:
        return "D"
    return "F"
