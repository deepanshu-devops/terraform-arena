# Deploying Terraform Arena on Render

The repository includes a Render Blueprint in `render.yaml`. It creates one
free Python web service named `terraform-arena`.

## Blueprint deploy

1. Sign in to <https://dashboard.render.com/>.
2. Open
   <https://render.com/deploy?repo=https://github.com/deepanshu-devops/terraform-arena>.
3. Connect the GitHub repository if Render asks.
4. Review the `terraform-arena` service and click **Apply**.

Render runs:

```text
Build: pip install --upgrade pip && pip install -r requirements.txt
Start: uvicorn app.main:app --host 0.0.0.0 --port $PORT
Health check: /api/health
```

Every push to `main` triggers a new deploy because `autoDeploy` is enabled.

## What the deployed service runs

- Static HCL grading. The Terraform CLI is intentionally **not** installed on
  the free Render service, so `ARENA_TERRAFORM=0`.
- Live AWS validation is disabled: `ARENA_ALLOW_APPLY=0`.
- No AWS credentials or secrets are stored in the repository or Render config.
- SQLite lives on the service's local filesystem.

## Free-plan storage

Render's free web service has an ephemeral filesystem. Progress and submission
history in `data/arena.db` survive while the instance is running, but reset when
the service spins down, redeploys, or is restarted.

For durable progress, upgrade to a paid instance and mount a persistent disk at
`/var/data`, then change the app's data directory to that path. The current
build keeps the free, zero-configuration setup.

## Manual service setup

If you prefer not to use the Blueprint:

1. Create a new **Web Service** from the GitHub repository.
2. Runtime: **Python**.
3. Build command: `pip install --upgrade pip && pip install -r requirements.txt`
4. Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Set `PYTHON_VERSION=3.12.10`, `ARENA_TERRAFORM=0`, and
   `ARENA_ALLOW_APPLY=0`.
6. Health check path: `/api/health`.

## Verify

After the deploy finishes, open the service URL and check:

```text
GET /api/health
```

Expected values include `"ok": true`, `"challenges": 117`, and
`"apply_enabled": false`.
