"""Catalog loader: compiles declarative specs into Challenge objects.

Numbering is assigned by the challenge registry after all hand-authored and
generated scenarios are merged.  Level 0 starts at 1.
"""
from __future__ import annotations

from functools import lru_cache

from ..declarative import build_challenge
from ..evaluator import Challenge
from .reference import (
    build_reference,
    choose_focus,
    level_for_spec,
    render_starter,
)

_CACHE: list[Challenge] | None = None


# ---------------------------------------------------------------------------
# Starter workspace scaffolding
# ---------------------------------------------------------------------------
def render_starter_files(spec: dict) -> dict[str, str]:
    """Return the complete configuration minus the one graded region."""
    return render_starter(spec)


def render_readme(challenge: Challenge) -> str:
    lines = [
        f"# {challenge.number:03d} - {challenge.title}",
        "",
        f"**Level:** {challenge.level_name or 'Unranked'}  ",
        f"**Difficulty:** {challenge.difficulty}  ",
        f"**Points:** {challenge.points}  ",
        f"**Tags:** {', '.join(challenge.tags)}",
        "",
        "## Scenario",
        "",
        challenge.scenario,
        "",
        "## What to complete",
        "",
    ]
    focus = challenge.focus or {}
    file_name = focus.get("file", "main.tf")
    lines.append(f"- File: `{file_name}`")
    lines.append(f"- Task: {focus.get('title', 'Complete the graded block')}")
    if focus.get("todo"):
        lines.append(f"- {focus['todo']}")
    lines += ["", "## Constraints", ""]
    lines += [f"- {c}" for c in challenge.constraints] or ["- None."]
    lines += ["", "## Input variables", "", "| Name | Type | Default |", "| --- | --- | --- |"]
    for v in challenge.variables:
        default = v.get("default", "required")
        lines.append(f"| `{v['name']}` | `{v.get('type', 'string')}` | `{default}` |")
    lines += ["", "## Expected resources", ""]
    lines += [f"- `{r}`" for r in challenge.expected_resources] or ["- (see constraints)"]
    lines += ["", "## Expected outputs", ""]
    lines += [f"- `{o}`" for o in challenge.expected_outputs] or ["- (none)"]
    lines += [
        "",
        "## How to test",
        "",
        "```powershell",
        f"python judge.py test {challenge.number} --dir workspaces/{challenge.number:03d}-{challenge.id}",
        "```",
        "",
        "> Hidden test details are only revealed after a submission.",
        "",
    ]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Compilation
# ---------------------------------------------------------------------------
def prepare_spec(spec: dict) -> dict:
    spec = dict(spec)
    spec.setdefault("starter", {})
    if "level" not in spec:
        level, level_name = level_for_spec(spec)
        spec["level"] = level
        spec["level_name"] = level_name
    else:
        spec.setdefault("level_name", level_for_spec(spec)[1])
    reference = spec.get("reference") or build_reference(spec)
    spec["reference"] = reference
    focus = choose_focus(spec)
    spec["focus"] = focus.public()
    spec["starter"] = render_starter(spec)
    return spec


def _sort_key(spec: dict) -> tuple[int, int, str]:
    level = spec.get("level")
    if level is None:
        level = level_for_spec(spec)[0]
    return (int(level), int(spec.get("points", 0)), spec.get("title", ""))


@lru_cache(maxsize=1)
def load_catalog() -> tuple[Challenge, ...]:
    global _CACHE
    if _CACHE is None:
        from .extra import all_specs

        built: list[Challenge] = []
        for index, raw_spec in enumerate(sorted(all_specs(), key=_sort_key)):
            spec = prepare_spec(raw_spec)
            number = index + 1
            spec["number"] = number
            built.append(build_challenge(spec, number))
        _CACHE = built
    return tuple(_CACHE)


def catalog_ids() -> list[str]:
    return [c.id for c in load_catalog()]
