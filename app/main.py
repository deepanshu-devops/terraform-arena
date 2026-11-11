"""FastAPI application: REST API + static HackerRank-style UI."""
from __future__ import annotations

import re
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from . import db, jobs, live, runner
from .challenges import all_challenges, challenge_count, get_challenge
from .evaluator import Challenge

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR.parent / "static"
MAX_FILE_BYTES = 200_000
SAFE_NAME = re.compile(r"^[A-Za-z0-9_.-]+\.tf$")


@asynccontextmanager
async def lifespan(app: FastAPI):
    db.init_db()
    db.seed_challenges(all_challenges())
    yield


app = FastAPI(
    title="Terraform Arena",
    description="Practice Terraform with instant, structured PASS/FAIL grading.",
    version="1.0.0",
    lifespan=lifespan,
)

if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


class SubmitRequest(BaseModel):
    challenge: str = Field(..., description="Challenge number or id")
    files: dict[str, str] = Field(..., description="filename -> HCL source")


@app.get("/", include_in_schema=False)
def index():
    target = STATIC_DIR / "index.html"
    if not target.exists():
        return {"message": "UI not built. API is available at /docs."}
    return FileResponse(target)


@app.get("/api/health")
def health():
    return {
        "ok": True,
        "challenges": challenge_count(),
        "terraform": runner.status(),
        "live": live.status(),
    }


@app.get("/api/stats")
def stats():
    user_id = db.default_user_id()
    data = db.stats(user_id)
    data["total_challenges"] = challenge_count()
    return data


@app.get("/api/challenges")
def list_challenges(
    difficulty: str | None = None,
    level: int | None = Query(default=None, ge=0, le=5),
    tag: str | None = None,
    search: str | None = None,
    limit: int = Query(default=500, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
):
    user_id = db.default_user_id()
    progress = db.all_progress(user_id)

    items = all_challenges()
    if difficulty:
        items = [c for c in items if c.difficulty.lower() == difficulty.lower()]
    if level is not None:
        items = [c for c in items if c.level == level]
    if tag:
        items = [c for c in items if tag.lower() in [t.lower() for t in c.tags]]
    if search:
        q = search.lower()
        items = [
            c
            for c in items
            if q in c.title.lower()
            or q in c.id.lower()
            or q in c.scenario.lower()
            or q in c.level_name.lower()
        ]
    items = sorted(items, key=lambda c: c.number)
    page = items[offset : offset + limit]

    return {
        "total": len(items),
        "items": [
            {
                "id": c.id,
                "number": c.number,
                "title": c.title,
                "difficulty": c.difficulty,
                "points": c.points,
                "level": c.level,
                "level_name": c.level_name,
                "focus": c.focus,
                "tags": c.tags,
                "test_count": len(c.tests) + 1,
                "progress": progress.get(c.id),
            }
            for c in page
        ],
    }


@app.get("/api/challenges/{key}")
def get_one(key: str):
    challenge = get_challenge(key)
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")
    user_id = db.default_user_id()
    payload = challenge.public()
    payload["progress"] = db.all_progress(user_id).get(challenge.id)
    return payload


@app.post("/api/submit")
def submit(request: SubmitRequest):
    challenge = get_challenge(request.challenge)
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")
    files = _validate_files(request.files)
    user_id = db.default_user_id()
    job_id = jobs.submit(user_id, challenge, files)
    return {"job_id": job_id, "challenge_id": challenge.id}


@app.get("/api/jobs/{job_id}")
def get_job(job_id: str):
    job = db.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return jobs.job_payload(job)


@app.get("/api/submissions")
def submissions(limit: int = Query(default=20, ge=1, le=100)):
    user_id = db.default_user_id()
    return {"items": db.recent_submissions(user_id, limit)}


@app.get("/api/submissions/{submission_id}")
def submission(submission_id: int):
    item = db.get_submission(submission_id)
    if not item:
        raise HTTPException(status_code=404, detail="Submission not found")
    return item


@app.get("/api/progress")
def progress():
    user_id = db.default_user_id()
    return db.all_progress(user_id)


@app.get("/api/terraform/status")
def terraform_status():
    return {**runner.status(), "live": live.status()}


def _validate_files(files: dict[str, str]) -> dict[str, str]:
    if not files:
        raise HTTPException(status_code=400, detail="No files supplied")
    clean: dict[str, str] = {}
    total = 0
    for name, content in files.items():
        if not SAFE_NAME.match(name):
            raise HTTPException(status_code=400, detail=f"Unsafe filename: {name!r}")
        if not isinstance(content, str):
            raise HTTPException(status_code=400, detail=f"{name} must be text")
        total += len(content.encode("utf-8"))
        if total > MAX_FILE_BYTES:
            raise HTTPException(status_code=413, detail="Submission is too large (200 KB cap)")
        clean[name] = content
    return clean
