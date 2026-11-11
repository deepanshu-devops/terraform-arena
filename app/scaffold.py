"""Build incomplete, structured starter workspaces.

Learners should spend their time on the graded arguments and wiring, not on
retyping provider boilerplate or variable declarations.  This module renders
valid HCL outlines: provider requirements, variable declarations with their
published defaults, one empty block per expected resource, and output
placeholders.  The resource bodies and output values are deliberately left
for the learner to complete.

Comments never include challenge titles or test assertions, so markers used
by textual checks are not satisfied by the scaffold itself.
"""
from __future__ import annotations

import json
import re
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .evaluator import Challenge

_MISSING = object()


def _hcl_literal(value: Any, indent: int = 0) -> str:
    """Render a Python value as a small HCL expression."""
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return repr(value)
    if isinstance(value, str):
        return json.dumps(value)
    if isinstance(value, (list, tuple)):
        if not value:
            return "[]"
        if all(isinstance(item, (str, int, float, bool)) or item is None for item in value):
            return "[" + ", ".join(_hcl_literal(item) for item in value) + "]"
        inner = ",\n".join(
            " " * (indent + 2) + _hcl_literal(item, indent + 2) for item in value
        )
        return "[\n" + inner + ",\n" + " " * indent + "]"
    if isinstance(value, dict):
        if not value:
            return "{}"
        lines = []
        for key, item in value.items():
            key_text = str(key)
            if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", key_text):
                key_text = json.dumps(key_text)
            lines.append(
                " " * (indent + 2) + f"{key_text} = {_hcl_literal(item, indent + 2)}"
            )
        return "{\n" + "\n".join(lines) + "\n" + " " * indent + "}"
    raise TypeError(f"Cannot render default value {value!r} as HCL")


def _variable_block(variable: dict) -> str:
    name = variable["name"]
    type_ = variable.get("type", "string")
    default = variable.get("default", _MISSING)

    lines = [
        f'variable "{name}" {{',
        f'  description = "Input variable {name}."',
        f"  type        = {type_}",
    ]
    if default is not _MISSING and default is not None:
        literal = _hcl_literal(default, 2)
        if "\n" in literal:
            lines.append(f"  default = {literal}")
        else:
            lines.append(f"  default     = {literal}")
    else:
        lines.append("  # TODO - add the published default if the scenario has one.")

    if variable.get("validation"):
        lines.extend(
            [
                "",
                "  validation {",
                "    # TODO - replace this placeholder with the rule from the problem statement.",
                f"    condition     = var.{name} != null",
                '    error_message = "Provide a valid value."',
                "  }",
            ]
        )

    lines.append("}")
    return "\n".join(lines)


def _versions_tf(provider: str, special: str) -> str:
    if special == "module":
        # No provider block here: the learner must decide what the module needs.
        return (
            "# versions.tf\n"
            "# TODO - add provider requirements if the scenario asks for them.\n"
            "terraform {\n"
            "}\n"
        )

    if special == "backend":
        return (
            "# versions.tf\n"
            "terraform {\n"
            '  required_version = ">= 1.3.0"\n'
            "\n"
            '  backend "s3" {\n'
            "    # TODO - fill in the backend settings.\n"
            "  }\n"
            "}\n"
        )

    if special in {"moved", "import"}:
        # Keep these files free of the textual markers used by the state tests.
        return (
            "# versions.tf\n"
            "# TODO - add provider requirements if the scenario asks for them.\n"
            "terraform {\n"
            "}\n"
        )

    if provider == "docker":
        return (
            "# versions.tf\n"
            "terraform {\n"
            '  required_version = ">= 1.3.0"\n'
            "\n"
            "  required_providers {\n"
            "    docker = {\n"
            '      source  = "kreuzwerker/docker"\n'
            '      version = "~> 3.0"\n'
            "    }\n"
            "  }\n"
            "}\n"
        )

    return (
        "# versions.tf\n"
        "terraform {\n"
        '  required_version = ">= 1.3.0"\n'
        "\n"
        "  required_providers {\n"
        "    aws = {\n"
        '      source  = "hashicorp/aws"\n'
        '      version = "~> 5.0"\n'
        "    }\n"
        "  }\n"
        "}\n"
    )


def _variables_tf(variables: list[dict]) -> str:
    if not variables:
        return "# variables.tf\n# This scenario does not require input variables.\n"
    blocks = [_variable_block(variable) for variable in variables]
    return "# variables.tf\n# Inputs are declared below.\n\n" + "\n\n".join(blocks) + "\n"


def _provider_block(provider: str, variables: list[dict]) -> str:
    names = {variable["name"] for variable in variables}
    if provider == "docker":
        if "docker_host" in names:
            return 'provider "docker" {\n  host = var.docker_host\n}\n'
        return (
            'provider "docker" {\n'
            "  # TODO - add provider settings if the scenario asks for them.\n"
            "}\n"
        )
    if provider == "aws":
        if "aws_region" in names:
            return 'provider "aws" {\n  region = var.aws_region\n}\n'
        return (
            'provider "aws" {\n'
            "  # TODO - add provider settings if the scenario asks for them.\n"
            "}\n"
        )
    return ""


def _main_tf(provider: str, resources: list[str], variables: list[dict], special: str) -> str:
    header = "# main.tf\n# Complete the TODO blocks below.\n\n"

    if special == "backend":
        return (
            "# main.tf\n"
            "# The remote state backend is configured in versions.tf.\n"
        )

    if special == "module":
        return (
            "# main.tf\n"
            "# Complete the module block below.\n\n"
            'module "this" {\n'
            "  # TODO - point this at the local module and pass the inputs.\n"
            "}\n"
        )

    if special == "moved":
        return (
            "# main.tf\n"
            "# Complete the block below.\n\n"
            "moved {\n"
            "  # TODO - complete this block.\n"
            "}\n"
        )

    if special == "import":
        return (
            "# main.tf\n"
            "# Complete the block below.\n\n"
            "import {\n"
            "  # TODO - complete this block.\n"
            "}\n"
        )

    provider_block = _provider_block(provider, variables)
    blocks = []
    for resource in resources:
        blocks.append(
            f'resource "{resource}" "this" {{\n'
            "  # TODO - add the arguments required by the problem statement.\n"
            "}\n"
        )

    if not blocks:
        blocks.append("# TODO - add the blocks required by the problem statement.\n")

    parts = [header.rstrip("\n")]
    if provider_block:
        parts.append(provider_block.rstrip("\n"))
    parts.extend(block.rstrip("\n") for block in blocks)
    return "\n\n".join(parts) + "\n"


def _outputs_tf(outputs: list[str]) -> str:
    if not outputs:
        return "# outputs.tf\n# This scenario does not require outputs.\n"

    blocks = []
    for name in outputs:
        blocks.append(
            f'output "{name}" {{\n'
            "  # TODO - replace null with the correct value reference.\n"
            "  value = null\n"
            "}\n"
        )
    return "# outputs.tf\n# Complete the output values below.\n\n" + "\n".join(blocks)


def _provider_for(resources: list[str]) -> str:
    if any(resource.startswith("docker_") for resource in resources):
        return "docker"
    return "aws"


def _special_for(challenge_id: str, number: int, resources: list[str]) -> str:
    if challenge_id == "state-s3-backend" or number == 102:
        return "backend"
    if challenge_id == "refactor-moved-block" or number == 104:
        return "moved"
    if challenge_id == "import-block" or number == 105:
        return "import"
    if "module" in resources or challenge_id.startswith("mod-"):
        return "module"
    return ""


def render_scaffold_parts(
    *,
    challenge_id: str,
    number: int,
    variables: list[dict],
    resources: list[str],
    outputs: list[str],
) -> dict[str, str]:
    """Render the four starter files from challenge metadata."""
    special = _special_for(challenge_id, number, resources)
    provider = _provider_for(resources)
    return {
        "versions.tf": _versions_tf(provider, special),
        "variables.tf": _variables_tf(variables),
        "main.tf": _main_tf(provider, resources, variables, special),
        "outputs.tf": _outputs_tf(outputs),
    }


def render_scaffold(challenge: "Challenge") -> dict[str, str]:
    """Render starter files for an already-built Challenge object."""
    return render_scaffold_parts(
        challenge_id=challenge.id,
        number=challenge.number,
        variables=challenge.variables,
        resources=challenge.expected_resources,
        outputs=challenge.expected_outputs,
    )
