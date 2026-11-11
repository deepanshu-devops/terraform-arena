"""Async evaluation queue.

Mirrors the production worker model (API enqueues -> worker evaluates ->
client polls) using a bounded ThreadPoolExecutor and the jobs table. Swapping
this for Redis/Celery later only requires replacing ``submit``.
"""
from __future__ import annotations

import uuid
from concurrent.futures import ThreadPoolExecutor
from typing import Any

from . import db, runner
from .evaluator import Challenge, evaluate

EXECUTOR = ThreadPoolExecutor(max_workers=2, thread_name_prefix="arena-worker")


def submit(user_id: int, challenge: Challenge, files: dict[str, str]) -> str:
    job_id = uuid.uuid4().hex
    db.create_job(job_id, user_id, challenge.id)
    EXECUTOR.submit(_run_job, job_id, user_id, challenge, files)
    return job_id


def _run_job(
    job_id: str, user_id: int, challenge: Challenge, files: dict[str, str]
) -> None:
    db.update_job(job_id, "running")
    try:
        result = evaluate(challenge, files)

        terraform = runner.validate_files(files)
        if terraform.get("ran"):
            result["terraform"] = terraform
            validation = terraform.get("validate") or {}
            if validation and not validation.get("ok"):
                result["status"] = "FAIL"
                result["tests"].append(
                    {
                        "id": "terraform-validate",
                        "title": "terraform validate",
                        "category": "Terraform",
                        "weight": 10,
                        "required": True,
                        "passed": False,
                        "detail": (validation.get("stderr") or validation.get("stdout") or "invalid")[:1500],
                    }
                )
                total_weight = sum(t["weight"] for t in result["tests"]) or 1
                passed_weight = sum(t["weight"] for t in result["tests"] if t["passed"])
                result["score"] = round(100 * passed_weight / total_weight)
                result["total"] = len(result["tests"])
                result["passed"] = sum(1 for t in result["tests"] if t["passed"])
        else:
            result["terraform"] = terraform

        submission_id = db.create_submission(user_id, challenge.id, files)
        db.finalize_submission(user_id, submission_id, result)
        db.update_job(
            job_id,
            "done",
            submission_id=submission_id,
            result=result,
        )
    except Exception as exc:  # pragma: no cover - defensive
        db.update_job(job_id, "error", error=f"{type(exc).__name__}: {exc}")


def job_payload(job: dict[str, Any]) -> dict:
    return {
        "id": job["id"],
        "state": job["state"],
        "challenge_id": job["challenge_id"],
        "submission_id": job["submission_id"],
        "error": job["error"],
        "result": job["result"],
        "created_at": job["created_at"],
        "updated_at": job["updated_at"],
    }
