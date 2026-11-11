"""Optional Terraform binary integration.

Static analysis is the default and needs no binary. When the real CLI is
installed *and* ``ARENA_TERRAFORM=1`` is set, submissions are additionally
checked with ``terraform init -backend=false`` + ``terraform validate``.

Live apply/destroy is intentionally gated behind ``ARENA_ALLOW_APPLY=1`` and
is only ever offered for the Docker sandbox challenges.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
from pathlib import Path

from .evaluator import Challenge

TEMP_ROOT = Path(__file__).resolve().parent.parent / "data" / "tmp"
TIMEOUT = 120


def terraform_binary() -> str | None:
    return shutil.which("terraform")


def enabled() -> bool:
    return os.environ.get("ARENA_TERRAFORM", "0") == "1"


def apply_enabled() -> bool:
    return os.environ.get("ARENA_ALLOW_APPLY", "0") == "1"


def status() -> dict:
    binary = terraform_binary()
    version = None
    if binary:
        try:
            proc = subprocess.run(
                [binary, "version", "-json"],
                capture_output=True,
                text=True,
                timeout=20,
            )
            if proc.returncode == 0:
                import json

                version = json.loads(proc.stdout).get("terraform_version")
        except Exception:
            version = None
    return {
        "available": bool(binary),
        "binary": binary,
        "version": version,
        "validation_enabled": bool(binary) and enabled(),
        "apply_enabled": bool(binary) and enabled() and apply_enabled(),
        "note": (
            "Install Terraform and set ARENA_TERRAFORM=1 to enable live validate/plan."
            if not binary
            else "Terraform detected. Static checks run by default."
        ),
    }


def _run(cmd: list[str], cwd: Path) -> dict:
    try:
        proc = subprocess.run(
            cmd,
            cwd=str(cwd),
            capture_output=True,
            text=True,
            timeout=TIMEOUT,
            env={**os.environ, "TF_IN_AUTOMATION": "1", "CHECKPOINT_DISABLE": "1"},
        )
        return {
            "ok": proc.returncode == 0,
            "code": proc.returncode,
            "stdout": (proc.stdout or "")[-6000:],
            "stderr": (proc.stderr or "")[-4000:],
        }
    except subprocess.TimeoutExpired:
        return {"ok": False, "code": -1, "stdout": "", "stderr": "timed out"}
    except Exception as exc:  # pragma: no cover - defensive
        return {"ok": False, "code": -1, "stdout": "", "stderr": str(exc)}


def validate_files(files: dict[str, str]) -> dict:
    """Run init + validate in an isolated temp directory. Never touches AWS."""
    binary = terraform_binary()
    if not binary:
        return {"ran": False, "reason": "terraform binary not installed"}
    if not enabled():
        return {"ran": False, "reason": "set ARENA_TERRAFORM=1 to enable live validation"}

    TEMP_ROOT.mkdir(parents=True, exist_ok=True)
    workdir = Path(tempfile.mkdtemp(prefix="arena-", dir=str(TEMP_ROOT)))
    try:
        for name, content in files.items():
            if not name.endswith(".tf"):
                continue
            (workdir / name).write_text(content, encoding="utf-8")
        init = _run([binary, "init", "-backend=false", "-input=false", "-no-color"], workdir)
        if not init["ok"]:
            return {"ran": True, "init": init, "validate": None}
        validate = _run([binary, "validate", "-no-color"], workdir)
        return {"ran": True, "init": init, "validate": validate}
    finally:
        shutil.rmtree(workdir, ignore_errors=True)


def apply_sandbox(challenge: Challenge, files: dict[str, str]) -> dict:
    """Reserved for Docker-only sandbox runs. Disabled by default."""
    if not challenge.apply_sandbox:
        return {"ran": False, "reason": "challenge is not sandbox-enabled"}
    if not apply_enabled():
        return {
            "ran": False,
            "reason": "set ARENA_TERRAFORM=1 and ARENA_ALLOW_APPLY=1 to enable apply",
        }
    return {"ran": False, "reason": "apply runner not enabled in this build"}
