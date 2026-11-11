"""SQLite persistence for Terraform Arena.

The schema mirrors the production blueprint (users / challenges / submissions /
test_results / jobs / progress) but uses the stdlib sqlite3 driver so the MVP
runs with zero infrastructure.
"""
from __future__ import annotations

import json
import os
import sqlite3
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterator

# ARENA_DATA_DIR lets a deployment point SQLite at a mounted persistent disk.
# Without one the data lives beside the app and is ephemeral on free hosts.
_DEFAULT_DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DATA_DIR = Path(os.getenv("ARENA_DATA_DIR", str(_DEFAULT_DATA_DIR))).expanduser()
DB_PATH = DATA_DIR / "arena.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    username    TEXT UNIQUE NOT NULL,
    email       TEXT,
    name        TEXT,
    avatar_url  TEXT,
    google_sub  TEXT,
    created_at  REAL NOT NULL,
    last_login  REAL
);

CREATE TABLE IF NOT EXISTS challenges (
    id          TEXT PRIMARY KEY,
    number      INTEGER NOT NULL,
    title       TEXT NOT NULL,
    difficulty  TEXT NOT NULL,
    points      INTEGER NOT NULL,
    tags        TEXT NOT NULL,
    test_count  INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS submissions (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id      INTEGER NOT NULL,
    challenge_id TEXT NOT NULL,
    status       TEXT NOT NULL,
    score        INTEGER NOT NULL,
    files        TEXT NOT NULL,
    result       TEXT NOT NULL,
    created_at   REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS test_results (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    submission_id INTEGER NOT NULL,
    test_id       TEXT NOT NULL,
    title         TEXT NOT NULL,
    category      TEXT NOT NULL,
    passed        INTEGER NOT NULL,
    detail        TEXT NOT NULL,
    weight        INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS jobs (
    id            TEXT PRIMARY KEY,
    user_id       INTEGER NOT NULL,
    challenge_id  TEXT NOT NULL,
    state         TEXT NOT NULL,
    error         TEXT,
    submission_id INTEGER,
    result        TEXT,
    created_at    REAL NOT NULL,
    updated_at    REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS progress (
    user_id      INTEGER NOT NULL,
    challenge_id TEXT NOT NULL,
    best_score   INTEGER NOT NULL DEFAULT 0,
    status       TEXT NOT NULL DEFAULT 'unsolved',
    attempts     INTEGER NOT NULL DEFAULT 0,
    solved_at    REAL,
    PRIMARY KEY (user_id, challenge_id)
);

CREATE INDEX IF NOT EXISTS idx_submissions_challenge ON submissions(challenge_id);
CREATE INDEX IF NOT EXISTS idx_jobs_challenge ON jobs(challenge_id);
"""

DEFAULT_USER = "local"


@contextmanager
def connect() -> Iterator[sqlite3.Connection]:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH, timeout=30)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def _migrate_users(conn: sqlite3.Connection) -> None:
    """Add the Google profile columns to databases created before auth."""
    columns = {
        str(row["name"]) for row in conn.execute("PRAGMA table_info(users)").fetchall()
    }
    additions = {
        "email": "TEXT",
        "name": "TEXT",
        "avatar_url": "TEXT",
        "google_sub": "TEXT",
        "last_login": "REAL",
    }
    for name, sql_type in additions.items():
        if name not in columns:
            conn.execute(f'ALTER TABLE users ADD COLUMN "{name}" {sql_type}')
    conn.execute(
        "CREATE UNIQUE INDEX IF NOT EXISTS idx_users_google_sub "
        "ON users(google_sub) WHERE google_sub IS NOT NULL"
    )


def init_db() -> None:
    with connect() as conn:
        conn.executescript(SCHEMA)
        _migrate_users(conn)
        conn.execute(
            "INSERT OR IGNORE INTO users (username, created_at) VALUES (?, ?)",
            (DEFAULT_USER, time.time()),
        )


def default_user_id() -> int:
    with connect() as conn:
        row = conn.execute(
            "SELECT id FROM users WHERE username = ?", (DEFAULT_USER,)
        ).fetchone()
        if row:
            return int(row["id"])
        cur = conn.execute(
            "INSERT INTO users (username, created_at) VALUES (?, ?)",
            (DEFAULT_USER, time.time()),
        )
        return int(cur.lastrowid)


def get_user(user_id: int) -> dict[str, Any] | None:
    with connect() as conn:
        row = conn.execute(
            "SELECT * FROM users WHERE id = ?", (user_id,)
        ).fetchone()
        if not row:
            return None
        data = dict(row)
        if data.get("google_sub"):
            data["display_name"] = data.get("name") or data.get("email") or "Learner"
        else:
            data["display_name"] = (
                data.get("name")
                or (
                    "Local learner"
                    if data.get("username") == DEFAULT_USER
                    else data.get("username")
                )
                or "Learner"
            )
        data["provider"] = "google" if data.get("google_sub") else "local"
        return data


def upsert_google_user(
    *,
    google_sub: str,
    email: str,
    name: str,
    avatar_url: str | None = None,
) -> dict[str, Any]:
    """Create or refresh the local profile linked to a Google subject.

    The stable Google ``sub`` is the identity key.  Email is display/contact
    metadata only, so account email changes do not create a second profile.
    """
    username = f"google:{google_sub}"
    now = time.time()
    with connect() as conn:
        row = conn.execute(
            "SELECT id FROM users WHERE google_sub = ? OR username = ? ORDER BY id LIMIT 1",
            (google_sub, username),
        ).fetchone()
        if row:
            user_id = int(row["id"])
            conn.execute(
                """
                UPDATE users
                SET google_sub = ?, email = ?, name = ?, avatar_url = ?,
                    last_login = ?, username = ?
                WHERE id = ?
                """,
                (google_sub, email, name, avatar_url, now, username, user_id),
            )
        else:
            cur = conn.execute(
                """
                INSERT INTO users
                    (username, email, name, avatar_url, google_sub, created_at, last_login)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (username, email, name, avatar_url, google_sub, now, now),
            )
            user_id = int(cur.lastrowid)
        stored = conn.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
        data = dict(stored)
        data["display_name"] = data.get("name") or data.get("email") or "Learner"
        data["provider"] = "google"
        return data


def list_profiles(limit: int = 100) -> list[dict[str, Any]]:
    """Leaderboard rows for every Google profile, newest activity first."""
    with connect() as conn:
        rows = conn.execute(
            """
            SELECT
                u.id,
                u.username,
                u.email,
                u.name,
                u.avatar_url,
                u.created_at,
                u.last_login,
                (SELECT COUNT(*) FROM progress p
                 WHERE p.user_id = u.id AND p.status = 'PASS') AS solved,
                (SELECT COUNT(*) FROM progress p
                 WHERE p.user_id = u.id) AS attempted,
                (SELECT COUNT(*) FROM submissions s
                 WHERE s.user_id = u.id) AS submissions,
                (SELECT AVG(s.score) FROM submissions s
                 WHERE s.user_id = u.id AND s.status != 'pending') AS average_score
            FROM users u
            WHERE u.google_sub IS NOT NULL
            ORDER BY solved DESC, submissions DESC, COALESCE(u.last_login, u.created_at) DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
        result: list[dict[str, Any]] = []
        for row in rows:
            data = dict(row)
            data["average_score"] = round(data["average_score"] or 0, 1)
            data["display_name"] = data.get("name") or data.get("email") or "Learner"
            result.append(data)
        return result


def seed_challenges(challenges) -> int:
    with connect() as conn:
        for challenge in challenges:
            conn.execute(
                """
                INSERT INTO challenges (id, number, title, difficulty, points, tags, test_count)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                    number=excluded.number,
                    title=excluded.title,
                    difficulty=excluded.difficulty,
                    points=excluded.points,
                    tags=excluded.tags,
                    test_count=excluded.test_count
                """,
                (
                    challenge.id,
                    challenge.number,
                    challenge.title,
                    challenge.difficulty,
                    challenge.points,
                    json.dumps(challenge.tags),
                    len(challenge.tests) + 1,
                ),
            )
    return len(challenges)


# ---------------------------------------------------------------------------
# Submissions
# ---------------------------------------------------------------------------
def create_submission(user_id: int, challenge_id: str, files: dict[str, str]) -> int:
    with connect() as conn:
        cur = conn.execute(
            """
            INSERT INTO submissions (user_id, challenge_id, status, score, files, result, created_at)
            VALUES (?, ?, 'pending', 0, ?, '{}', ?)
            """,
            (user_id, challenge_id, json.dumps(files), time.time()),
        )
        return int(cur.lastrowid)


def finalize_submission(user_id: int, submission_id: int, result: dict) -> None:
    with connect() as conn:
        conn.execute(
            "UPDATE submissions SET status = ?, score = ?, result = ? WHERE id = ?",
            (result["status"], result["score"], json.dumps(result), submission_id),
        )
        conn.executemany(
            """
            INSERT INTO test_results
                (submission_id, test_id, title, category, passed, detail, weight)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    submission_id,
                    t["id"],
                    t["title"],
                    t["category"],
                    1 if t["passed"] else 0,
                    t["detail"],
                    t["weight"],
                )
                for t in result["tests"]
            ],
        )
        _update_progress(conn, user_id, result["challenge_id"], result["status"], result["score"])


def _update_progress(
    conn: sqlite3.Connection, user_id: int, challenge_id: str, status: str, score: int
) -> None:
    row = conn.execute(
        "SELECT best_score, status, attempts FROM progress WHERE user_id = ? AND challenge_id = ?",
        (user_id, challenge_id),
    ).fetchone()
    now = time.time()
    if row is None:
        conn.execute(
            """
            INSERT INTO progress (user_id, challenge_id, best_score, status, attempts, solved_at)
            VALUES (?, ?, ?, ?, 1, ?)
            """,
            (user_id, challenge_id, score, status, now if status == "PASS" else None),
        )
        return
    best = max(int(row["best_score"]), score)
    solved = row["status"] == "PASS" or status == "PASS"
    conn.execute(
        """
        UPDATE progress
        SET best_score = ?, status = ?, attempts = attempts + 1,
            solved_at = CASE WHEN ? THEN COALESCE(solved_at, ?) ELSE solved_at END
        WHERE user_id = ? AND challenge_id = ?
        """,
        (
            best,
            "PASS" if solved else "FAIL",
            1 if solved else 0,
            now,
            user_id,
            challenge_id,
        ),
    )


def get_submission(submission_id: int) -> dict[str, Any] | None:
    with connect() as conn:
        row = conn.execute(
            "SELECT * FROM submissions WHERE id = ?", (submission_id,)
        ).fetchone()
        if not row:
            return None
        data = dict(row)
        data["files"] = json.loads(data["files"])
        data["result"] = json.loads(data["result"])
        return data


def recent_submissions(user_id: int, limit: int = 20) -> list[dict[str, Any]]:
    with connect() as conn:
        rows = conn.execute(
            """
            SELECT s.id, s.challenge_id, s.status, s.score, s.created_at, c.number, c.title
            FROM submissions s
            LEFT JOIN challenges c ON c.id = s.challenge_id
            WHERE s.user_id = ?
            ORDER BY s.id DESC
            LIMIT ?
            """,
            (user_id, limit),
        ).fetchall()
        return [dict(r) for r in rows]


# ---------------------------------------------------------------------------
# Jobs
# ---------------------------------------------------------------------------
def create_job(job_id: str, user_id: int, challenge_id: str) -> None:
    now = time.time()
    with connect() as conn:
        conn.execute(
            """
            INSERT INTO jobs (id, user_id, challenge_id, state, created_at, updated_at)
            VALUES (?, ?, ?, 'queued', ?, ?)
            """,
            (job_id, user_id, challenge_id, now, now),
        )


def update_job(
    job_id: str,
    state: str,
    *,
    error: str | None = None,
    submission_id: int | None = None,
    result: dict | None = None,
) -> None:
    with connect() as conn:
        conn.execute(
            """
            UPDATE jobs
            SET state = ?, error = COALESCE(?, error),
                submission_id = COALESCE(?, submission_id),
                result = COALESCE(?, result), updated_at = ?
            WHERE id = ?
            """,
            (
                state,
                error,
                submission_id,
                json.dumps(result) if result is not None else None,
                time.time(),
                job_id,
            ),
        )


def get_job(job_id: str) -> dict[str, Any] | None:
    with connect() as conn:
        row = conn.execute("SELECT * FROM jobs WHERE id = ?", (job_id,)).fetchone()
        if not row:
            return None
        data = dict(row)
        data["result"] = json.loads(data["result"]) if data["result"] else None
        return data


# ---------------------------------------------------------------------------
# Progress / stats
# ---------------------------------------------------------------------------
def all_progress(user_id: int) -> dict[str, dict]:
    with connect() as conn:
        rows = conn.execute(
            "SELECT * FROM progress WHERE user_id = ?", (user_id,)
        ).fetchall()
        return {r["challenge_id"]: dict(r) for r in rows}


def stats(user_id: int) -> dict[str, Any]:
    with connect() as conn:
        total = conn.execute("SELECT COUNT(*) AS n FROM challenges").fetchone()["n"]
        solved = conn.execute(
            "SELECT COUNT(*) AS n FROM progress WHERE user_id = ? AND status = 'PASS'",
            (user_id,),
        ).fetchone()["n"]
        attempted = conn.execute(
            "SELECT COUNT(*) AS n FROM progress WHERE user_id = ?", (user_id,)
        ).fetchone()["n"]
        submissions = conn.execute(
            "SELECT COUNT(*) AS n FROM submissions WHERE user_id = ?", (user_id,)
        ).fetchone()["n"]
        avg = conn.execute(
            "SELECT AVG(score) AS a FROM submissions WHERE user_id = ? AND status != 'pending'",
            (user_id,),
        ).fetchone()["a"]
        by_difficulty = conn.execute(
            """
            SELECT c.difficulty, COUNT(*) AS total,
                   SUM(CASE WHEN p.status = 'PASS' THEN 1 ELSE 0 END) AS solved
            FROM challenges c
            LEFT JOIN progress p ON p.challenge_id = c.id AND p.user_id = ?
            GROUP BY c.difficulty
            """,
            (user_id,),
        ).fetchall()
        return {
            "total_challenges": total,
            "solved": solved,
            "attempted": attempted,
            "submissions": submissions,
            "average_score": round(avg or 0, 1),
            "by_difficulty": [dict(r) for r in by_difficulty],
        }
