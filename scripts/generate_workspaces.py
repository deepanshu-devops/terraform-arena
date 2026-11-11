#!/usr/bin/env python3
"""Generate the physical workspaces/ directory for every challenge.

Each folder contains incomplete .tf files, a README with the statement,
and challenge.json metadata.  Folders are keyed by stable challenge id, so a
catalog renumbering renames the old folder instead of orphaning it.  Learner-
edited files are preserved; untouched starters are refreshed.
"""
from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app.challenges import all_challenges  # noqa: E402
from app.workspace import (  # noqa: E402
    WORKSPACES,
    _previous_starter,
    refresh_workspace_starters,
    workspace_dir,
)

_FOLDER = re.compile(r"^\d{3}-(.+)$")


def migrate_folders(challenges) -> list[tuple[str, str]]:
    """Move legacy numbered folders to their current number, by stable id.

    If both the old and new folder already exist, user-edited files from the
    old folder are copied only when the new folder still holds an untouched
    starter.  Nothing is deleted unless the old folder ends up empty.
    """
    by_id = {challenge.id: challenge for challenge in challenges}
    moved: list[tuple[str, str]] = []
    if not WORKSPACES.exists():
        return moved

    for entry in sorted(WORKSPACES.iterdir()):
        if not entry.is_dir():
            continue
        match = _FOLDER.match(entry.name)
        if not match:
            continue
        challenge = by_id.get(match.group(1))
        if challenge is None:
            continue
        target = workspace_dir(challenge)
        if entry.resolve() == target.resolve():
            continue

        target.parent.mkdir(parents=True, exist_ok=True)
        if not target.exists():
            entry.rename(target)
            moved.append((entry.name, target.name))
            continue

        old_starters = _previous_starter(entry)
        new_starters = _previous_starter(target)
        for source in sorted(entry.iterdir()):
            if not source.is_file():
                continue
            dest = target / source.name
            if not dest.exists():
                shutil.move(str(source), str(dest))
                continue
            if source.suffix != ".tf":
                continue
            old_text = source.read_text(encoding="utf-8")
            new_text = dest.read_text(encoding="utf-8")
            old_untouched = old_starters.get(source.name, "").strip() == old_text.strip()
            new_untouched = new_starters.get(source.name, "").strip() == new_text.strip()
            if not old_untouched and new_untouched:
                shutil.copy2(source, dest)
        try:
            entry.rmdir()
        except OSError:
            pass
        moved.append((entry.name, target.name + " (merged)"))
    return moved


def generate(force: bool = False) -> int:
    challenges = all_challenges()
    WORKSPACES.mkdir(parents=True, exist_ok=True)
    migrate_folders(challenges)

    rows: list[str] = [
        "# Terraform Arena - Challenge Index",
        "",
        f"{len(challenges)} challenges, ordered from level 0 (HCL basics) to level 5 (capstones).",
        "",
        "| # | Level | Difficulty | Points | Challenge | Focus | Folder |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]

    for challenge in challenges:
        folder = workspace_dir(challenge)
        folder.mkdir(parents=True, exist_ok=True)
        refresh_workspace_starters(challenge, force=force)
        focus = challenge.focus or {}
        focus_label = focus.get("title") or "Complete the graded block"
        rows.append(
            f"| {challenge.number:03d} | {challenge.level_name} | {challenge.difficulty} "
            f"| {challenge.points} | {challenge.title} | {focus_label} "
            f"| `{folder.name}` |"
        )

    (WORKSPACES / "INDEX.md").write_text(
        "\n".join(rows) + "\n", encoding="utf-8", newline="\n"
    )

    readme = [
        "# Terraform Arena Workspaces",
        "",
        "Each numbered folder is one challenge. The surrounding configuration is",
        "complete; fill in the single TODO block described in the folder README,",
        "then run:",
        "",
        "```powershell",
        "python judge.py test <number>",
        "```",
        "",
        "Level 0 starts with HCL fundamentals. Level 5 contains the capstones.",
        "See `INDEX.md` for the full catalog and the focus block for each challenge.",
        "",
    ]
    (WORKSPACES / "README.md").write_text(
        "\n".join(readme), encoding="utf-8", newline="\n"
    )
    return len(challenges)


if __name__ == "__main__":
    force = "--force" in sys.argv[1:]
    count = generate(force=force)
    print(f"Generated {count} workspaces under {WORKSPACES}")
