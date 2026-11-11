"""SQLite persistence for Terraform Arena.

The schema mirrors the production blueprint (users / challenges / submissions /
test_results / jobs / progress) but uses the stdlib sqlite3 driver so the MVP
runs with zero infrastructure.
"""
from __future__ import annotations

import json
import sqlite3
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterator

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DB_PATH = DATA_DIR / "arena.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    username    TEXT UNIQUE NOT NULL,
    created_at  REAL NOT NULL
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


def init_db() -> None:
    with connect() as conn:
        conn.executescript(SCHEMA)
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
