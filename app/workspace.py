"""Workspace export helpers shared by the CLI and the generator."""
from __future__ import annotations

import json
from pathlib import Path

from .catalog import render_readme
from .evaluator import Challenge

ROOT = Path(__file__).resolve().parent.parent
WORKSPACES = ROOT / "workspaces"


def workspace_dir(challenge: Challenge) -> Path:
    return WORKSPACES / f"{challenge.number:03d}-{challenge.id}"


def write_workspace(challenge: Challenge, force: bool = False) -> Path:
    folder = workspace_dir(challenge)
    folder.mkdir(parents=True, exist_ok=True)
    for name, content in challenge.starter.items():
        target = folder / name
        if target.exists() and not force:
            continue
        target.write_text(content, encoding="utf-8", newline="\n")
    # README and challenge.json are generated metadata, so keep them in sync
    # with the catalog even when learner-authored .tf files are preserved.
    readme = folder / "README.md"
    readme.write_text(render_readme(challenge), encoding="utf-8", newline="\n")
    meta = folder / "challenge.json"
    meta.write_text(json.dumps(challenge.public(), indent=2), encoding="utf-8")
    return folder


def read_workspace(folder: Path) -> dict[str, str]:
    files: dict[str, str] = {}
    if not folder.exists():
        return files
    for path in sorted(folder.glob("*.tf")):
        files[path.name] = path.read_text(encoding="utf-8")
    return files


def is_comment_only(text: str) -> bool:
    """True when a file contains only blank lines and comments.

    This is used by ``refresh-starters`` to replace untouched starter files
    without touching a workspace where the learner has started writing HCL.
    """
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("#") or stripped.startswith("//"):
            continue
        return False
    return True


def _previous_starter(folder: Path) -> dict[str, str]:
    """Read the starter snapshot embedded in a workspace's challenge.json.

    The snapshot lets a refresh distinguish an untouched starter (safe to
    replace) from a file the learner has edited (must be preserved), even when
    the starter itself contains real HCL rather than only comments.
    """
    meta = folder / "challenge.json"
    if not meta.exists():
        return {}
    try:
        data = json.loads(meta.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    starter = data.get("starter")
    if not isinstance(starter, dict):
        return {}
    return {str(k): str(v) for k, v in starter.items()}


def refresh_workspace_starters(
    challenge: Challenge,
    *,
    force: bool = False,
    dry_run: bool = False,
) -> tuple[list[str], list[str]]:
    """Refresh .tf starters while preserving files that contain learner code.

    A file is considered untouched when it is comment-only or byte-for-byte
    equal (ignoring outer whitespace) to the starter recorded in its
    ``challenge.json`` snapshot.  Everything else is treated as learner work.

    Returns ``(updated, preserved)`` file-name lists.
    """
    folder = workspace_dir(challenge)
    folder.mkdir(parents=True, exist_ok=True)
    previous = _previous_starter(folder)

    updated: list[str] = []
    preserved: list[str] = []

    for name, content in challenge.starter.items():
        target = folder / name
        if not target.exists():
            if not dry_run:
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(content, encoding="utf-8", newline="\n")
            updated.append(name)
            continue

        existing = target.read_text(encoding="utf-8")
        if existing.strip() == content.strip():
            continue

        old = previous.get(name)
        untouched = old is not None and existing.strip() == old.strip()

        if force or untouched or is_comment_only(existing):
            if not dry_run:
                target.write_text(content, encoding="utf-8", newline="\n")
            updated.append(name)
        else:
            preserved.append(name)

    # challenge.json and README are generated metadata (challenge.json embeds
    # the starter files), so keep them in sync even when learner code is
    # preserved.
    if not dry_run:
        meta = folder / "challenge.json"
        meta.write_text(json.dumps(challenge.public(), indent=2), encoding="utf-8")
        (folder / "README.md").write_text(
            render_readme(challenge), encoding="utf-8", newline="\n"
        )

    return updated, preserved
