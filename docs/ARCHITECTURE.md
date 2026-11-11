# Architecture

Terraform Arena is built so the expensive, dangerous part of grading can be
swapped in later without touching the API or UI. The default path is 100%
static and offline.

## Production blueprint

```
              ┌──────────────────────┐
  browser ───▶│  API (FastAPI)       │
              │  auth · catalog      │
              │  submit · poll       │
              └───────┬──────────────┘
                      │ enqueue job (id, user, challenge, artifact ref)
                      ▼
              ┌──────────────────────┐
              │  Queue               │
              │  Redis / RabbitMQ    │
              └───────┬──────────────┘
                      │
        ┌─────────────┼─────────────┐
        ▼             ▼             ▼
 ┌────────────┐ ┌────────────┐ ┌────────────┐
 │ worker 1   │ │ worker 2   │ │ worker N   │   Docker, no inbound network
 │ ephemeral  │ │ ephemeral  │ │ ephemeral  │   one submission per container
 └─────┬──────┘ └─────┬──────┘ └─────┬──────┘
       │              │              │
       ▼              ▼              ▼
   static HCL      terraform      security
   test suite      init/validate   Trivy / TFSec
                   plan (dry)      policy checks
       │
       ▼
   result JSON ──▶ Postgres (submissions, test_results, progress)
       │
       └──────────▶ object storage (artifacts, plans, logs)
```

### Submission lifecycle

1. `POST /api/submit` validates filenames and total size, writes a `jobs` row
   with `state=queued`, and returns a job id immediately.
2. A worker claims the job (`queued -> running`) and materializes the files in
   a fresh temporary directory. The directory is the only writable mount.
3. The worker runs the test tiers in order, stopping on a hard failure:
   - **Static**: parse HCL, run the challenge's hidden test manifest, policy
     allowlist, syntax/formatting/variable/drift grading. Never touches cloud.
   - **Terraform validate / plan**: `init -backend=false`, `validate`,
     `plan -refresh=false` with fake credentials and `-lock=false`.
   - **Sandbox apply** (opt-in, Docker provider only): `apply`, run health
     probes, then **always** `terraform destroy -auto-approve` in a `finally`
     block. A reaper process destroys any sandbox older than the hard timeout.
   - **Security**: Trivy config scan and TFSec rules, normalized into the same
     `blocked` / `warnings` shape the static engine returns.
4. Test rows are persisted individually (`test_results`), progress is updated
   (`best_score`, `status`, `attempts`), and the job becomes `done` or `error`.
5. The client polls `GET /api/jobs/{id}` and renders the structured verdict.

### Isolation and cost controls

- One worker container per submission; no shared `/tmp`, no inbound network.
- Hard wall-clock timeout (default 10 min) and per-command timeout (120 s).
- Resource caps: at most 60 resources, at most 20 instances from a single
  `count`/`for_each`, free-tier instance types only.
- Blocked resource types and providers (spot fleets, SageMaker endpoints, etc.).
- Blocked `local-exec` / `remote-exec`; no arbitrary shell execution.
- Hardcoded credential detection (`AKIA...`, provider `access_key` / `secret_key`
  / `token`).
- AWS runs are disabled by default. Live validation requires both
  `ARENA_TERRAFORM=1` and, for Docker sandboxes, `ARENA_ALLOW_APPLY=1`.
- Every apply path has a matching destroy path, and the destroy runs even when
  the apply partially fails.

### Why an async queue at all?

Evaluation is milliseconds today, but the contract is already asynchronous:
the API never blocks on a worker, the client polls a job, and results are
durable. Moving to Redis + Celery/RQ or RabbitMQ is a replacement of
`app/jobs.py` only. The SQLite schema already mirrors the production tables.

## MVP mapping

| Blueprint piece | This build | Swap path |
| --- | --- | --- |
| API | FastAPI (`app/main.py`) | unchanged |
| Queue | `ThreadPoolExecutor` + `jobs` table (`app/jobs.py`) | Redis + Celery/RQ |
| Database | SQLite (`app/db.py`) | Postgres (same tables) |
| Workers | in-process threads | Dockerized workers |
| Static tests | custom HCL parser + declarative checks | unchanged |
| Terraform validate | optional `app/runner.py` | same, containerized |
| Sandbox apply | gated placeholder | Docker provider + destroy reaper |
| Security scan | policy engine in `app/evaluator.py` | Trivy + TFSec |
| Artifacts | result JSON in SQLite | S3/MinIO + signed URLs |
| UI | vanilla JS (`static/`) | unchanged, or React later |

## Data model

```
users(id, username, created_at)
challenges(id, number, title, difficulty, points, tags, test_count)
submissions(id, user_id, challenge_id, status, score, files, result, created_at)
test_results(id, submission_id, test_id, title, category, passed, detail, weight)
jobs(id, user_id, challenge_id, state, error, submission_id, result, created_at, updated_at)
progress(user_id, challenge_id, best_score, status, attempts, solved_at)
```

`test_results` is the audit trail: every hidden assertion is persisted with
its weight and message, so a verdict can be replayed without re-running the
submission.

## Test tiers

| Tier | Runs by default | Cost | Purpose |
| --- | --- | --- | --- |
| HCL syntax | yes | free | brace balance, unterminated strings, duplicate attrs |
| Declarative hidden tests | yes | free | resources, attributes, references, nested blocks |
| Policy / security | yes | free | allowlists, credentials, wildcards, shell execution |
| Formatting | yes | free | fmt-style conventions |
| Variable compliance | yes | free | declared, typed, defaulted, validated, used |
| Architecture drift | yes | free | expected/missing/unexpected resources |
| `terraform validate` | opt-in | free | real provider schema validation |
| `terraform plan` | opt-in | free | graph + expression evaluation |
| Docker apply + destroy | opt-in | free | end-to-end container behaviour |
| Trivy / TFSec | future | free | external security rules |

## Adding a new tier

1. Produce a `(passed, detail)` or normalized result dict.
2. Append it to `result["tests"]` (or `result["security"]` for policy output).
3. Recompute `score`, `passed`, `total` if weights changed.
4. Keep every external command inside a timeout + `finally` cleanup.
