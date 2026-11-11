"""FastAPI application: REST API + static HackerRank-style UI."""
from __future__ import annotations

import re
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from starlette.middleware.sessions import SessionMiddleware

from . import auth, db, jobs, live, runner
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

app.add_middleware(
    SessionMiddleware,
    secret_key=auth.session_secret(),
    session_cookie=auth.SESSION_COOKIE,
    max_age=14 * 24 * 60 * 60,
    same_site="lax",
    https_only=auth.https_only(),
)

if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


def _public_user(user: dict | None) -> dict | None:
    """Expose only profile fields the browser needs, never the Google subject."""
    if not user:
        return None
    return {
        "id": user["id"],
        "display_name": user.get("display_name") or user.get("name") or "Learner",
        "email": user.get("email"),
        "avatar_url": user.get("avatar_url"),
        "provider": user.get("provider", "local"),
        "created_at": user.get("created_at"),
        "last_login": user.get("last_login"),
    }


def _current_user(request: Request) -> dict | None:
    """Return the signed-in profile, or the local profile in offline mode."""
    if not auth.auth_enabled():
        return db.get_user(db.default_user_id())
    user_id = request.session.get("user_id")
    if not user_id:
        return None
    user = db.get_user(int(user_id))
    if not user:
        request.session.clear()
    return user


def _require_user(request: Request) -> dict:
    user = _current_user(request)
    if user is None:
        if auth.auth_enabled():
            raise HTTPException(
                status_code=401,
                detail="Sign in with Google to save progress and submit solutions.",
            )
        user = db.get_user(db.default_user_id())
    if user is None:  # pragma: no cover - only possible on a broken database
        raise HTTPException(status_code=503, detail="Profile database is unavailable.")
    return user


def _empty_stats() -> dict:
    return {
        "total_challenges": challenge_count(),
        "solved": 0,
        "attempted": 0,
        "submissions": 0,
        "average_score": 0,
        "by_difficulty": [],
        "authenticated": False,
        "auth_enabled": auth.auth_enabled(),
    }


def _oauth_error(message: str) -> RedirectResponse:
    from urllib.parse import urlencode

    return RedirectResponse(
        "/?" + urlencode({"auth_error": message[:240]}),
        status_code=303,
    )


@app.get("/auth/google/login", include_in_schema=False)
def google_login(request: Request):
    if not auth.auth_enabled():
        raise HTTPException(
            status_code=503,
            detail=(
                "Google sign-in is not configured. Set GOOGLE_CLIENT_ID and "
                "GOOGLE_CLIENT_SECRET, or use the local profile."
            ),
        )
    state, verifier, nonce = auth.new_login_state()
    request.session["oauth_state"] = state
    request.session["oauth_code_verifier"] = verifier
    request.session["oauth_nonce"] = nonce
    return RedirectResponse(
        auth.authorization_url(
            state=state,
            code_verifier=verifier,
            nonce=nonce,
            redirect=auth.redirect_uri(request),
        ),
        status_code=302,
    )


@app.get("/auth/google/callback", name="google_callback", include_in_schema=False)
def google_callback(request: Request):
    if not auth.auth_enabled():
        return _oauth_error("Google sign-in is not configured on this deployment.")

    expected_state = request.session.pop("oauth_state", None)
    verifier = request.session.pop("oauth_code_verifier", None)
    nonce = request.session.pop("oauth_nonce", None)

    error = request.query_params.get("error")
    if error:
        detail = request.query_params.get("error_description") or error
        return _oauth_error(f"Google sign-in was cancelled: {detail}")

    state = request.query_params.get("state")
    code = request.query_params.get("code")
    if not code or not state or state != expected_state:
        return _oauth_error("The Google sign-in response was invalid or expired.")

    try:
        info = auth.exchange_code(
            code=code,
            code_verifier=verifier,
            redirect=auth.redirect_uri(request),
            nonce=nonce,
        )
        user = db.upsert_google_user(
            google_sub=str(info["sub"]),
            email=str(info.get("email", "")),
            name=str(info.get("name") or info.get("email") or "Learner"),
            avatar_url=info.get("picture"),
        )
    except auth.AuthError as exc:
        return _oauth_error(str(exc))

    request.session.clear()
    request.session["user_id"] = user["id"]
    return RedirectResponse("/", status_code=303)


@app.get("/auth/logout", include_in_schema=False)
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/", status_code=303)


@app.get("/api/auth/me")
def auth_me(request: Request):
    user = _current_user(request)
    return {
        "auth_enabled": auth.auth_enabled(),
        "authenticated": user is not None,
        "user": _public_user(user),
        "mode": "google" if auth.auth_enabled() else "local",
    }


@app.get("/api/profiles")
def profiles(request: Request, limit: int = Query(default=100, ge=1, le=500)):
    viewer = _require_user(request)
    if not auth.auth_enabled():
        data = db.stats(viewer["id"])
        return {
            "items": [
                {
                    "id": viewer["id"],
                    "display_name": viewer.get("display_name") or "Local learner",
                    "avatar_url": None,
                    "solved": data["solved"],
                    "attempted": data["attempted"],
                    "submissions": data["submissions"],
                    "average_score": data["average_score"],
                    "last_login": viewer.get("last_login"),
                    "is_self": True,
                    "email": None,
                }
            ],
            "total": 1,
            "viewer_id": viewer["id"],
        }

    rows = db.list_profiles(limit)
    items = []
    for row in rows:
        item = {
            "id": row["id"],
            "display_name": row["display_name"],
            "avatar_url": row.get("avatar_url"),
            "solved": row["solved"],
            "attempted": row["attempted"],
            "submissions": row["submissions"],
            "average_score": row["average_score"],
            "last_login": row.get("last_login"),
            "is_self": row["id"] == viewer["id"],
        }
        if item["is_self"]:
            item["email"] = row.get("email")
        items.append(item)
    return {"items": items, "total": len(items), "viewer_id": viewer["id"]}


class SubmitRequest(BaseModel):
    challenge: str = Field(..., description="Challenge number or id")
    files: dict[str, str] = Field(..., description="filename -> HCL source")


@app.get("/", include_in_schema=False)
def index():
    target = STATIC_DIR / "index.html"
    if not target.exists():
        return {"message": "UI not built. API is available at /docs."}
    return FileResponse(target)


@app.get("/health", include_in_schema=False)
@app.get("/healthz", include_in_schema=False)
@app.get("/api/health")
def health():
    return {
        "ok": True,
        "challenges": challenge_count(),
        "terraform": runner.status(),
        "live": live.status(),
        "auth": {"enabled": auth.auth_enabled()},
    }


@app.get("/api/stats")
def stats(request: Request):
    user = _current_user(request)
    if user is None:
        return _empty_stats()
    data = db.stats(user["id"])
    data["total_challenges"] = challenge_count()
    data["authenticated"] = True
    data["auth_enabled"] = auth.auth_enabled()
    return data


@app.get("/api/challenges")
def list_challenges(
    request: Request,
    difficulty: str | None = None,
    level: int | None = Query(default=None, ge=0, le=5),
    tag: str | None = None,
    search: str | None = None,
    limit: int = Query(default=500, ge=1, le=500),
    offset: int = Query(default=0, ge=0),
):
    user = _current_user(request)
    progress = db.all_progress(user["id"]) if user else {}

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
        "authenticated": user is not None,
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
def get_one(key: str, request: Request):
    challenge = get_challenge(key)
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")
    user = _current_user(request)
    payload = challenge.public()
    payload["progress"] = (
        db.all_progress(user["id"]).get(challenge.id) if user else None
    )
    return payload


@app.post("/api/submit")
def submit(request: Request, payload: SubmitRequest):
    user = _require_user(request)
    challenge = get_challenge(payload.challenge)
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")
    files = _validate_files(payload.files)
    job_id = jobs.submit(user["id"], challenge, files)
    return {"job_id": job_id, "challenge_id": challenge.id}


@app.get("/api/jobs/{job_id}")
def get_job(job_id: str, request: Request):
    user = _require_user(request)
    job = db.get_job(job_id)
    if not job or job.get("user_id") != user["id"]:
        raise HTTPException(status_code=404, detail="Job not found")
    return jobs.job_payload(job)


@app.get("/api/submissions")
def submissions(request: Request, limit: int = Query(default=20, ge=1, le=100)):
    user = _require_user(request)
    return {"items": db.recent_submissions(user["id"], limit)}


@app.get("/api/submissions/{submission_id}")
def submission(submission_id: int, request: Request):
    user = _require_user(request)
    item = db.get_submission(submission_id)
    if not item or item.get("user_id") != user["id"]:
        raise HTTPException(status_code=404, detail="Submission not found")
    return item


@app.get("/api/progress")
def progress(request: Request):
    user = _current_user(request)
    return db.all_progress(user["id"]) if user else {}


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
