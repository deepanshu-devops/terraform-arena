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

Every push to `main` triggers a new deploy because `autoDeploy` is enabled. If a
push does not start a deploy, open the service's **Events** tab and use
**Manual Deploy > Deploy latest commit**. A paused or disconnected GitHub
connection is the usual cause.

## What the deployed service runs

- Static HCL grading. The Terraform CLI is intentionally **not** installed on
  the free Render service, so `ARENA_TERRAFORM=0`.
- Live AWS validation is disabled: `ARENA_ALLOW_APPLY=0`.
- No AWS credentials or secrets are stored in the repository or Render config.
- SQLite lives on the service's local filesystem.

## Google sign-in

Google sign-in is optional. The app disables it automatically when credentials
are absent and keeps using the offline `local` profile. To enable it:

1. Create an OAuth 2.0 **Web application** client in
   <https://console.cloud.google.com/apis/credentials>.
2. Add the authorized redirect URI:
   `https://terraform-arena.onrender.com/auth/google/callback` (or your custom
   domain).
3. In the Render service, open **Environment** and set:
   - `GOOGLE_CLIENT_ID`
   - `GOOGLE_CLIENT_SECRET`
   - `GOOGLE_REDIRECT_URI` (same value as the Google redirect URI)
   - `ARENA_SECRET_KEY` (a long random value; used to sign session cookies)
   - `ARENA_HTTPS_ONLY=1`
4. Save the environment changes. Render restarts the service automatically.

The Blueprint declares `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` with
`sync: false`, so they are managed in the dashboard and never committed. If they
are missing, the header shows the local profile instead of a sign-in button.

Sessions use signed cookies and are scoped to the stable Google subject id.
Google is used only for identity; every learner's progress remains in SQLite.
Signing in does **not** write progress into the Google account or Google Drive.
The Google subject id links the account to a row in the server database, so
progress lasts only as long as that database lasts. On the free plan the
database is ephemeral (see below); on a paid plan with a persistent disk it
survives restarts and redeploys.

## Free-plan storage

Render's free web service has an ephemeral filesystem. Progress and submission
history in `data/arena.db` survive while the instance is running, but reset when
the service spins down, redeploys, or is restarted.

For durable progress, upgrade to a paid instance and mount a persistent disk at
`/var/data`, then set `ARENA_DATA_DIR=/var/data`. The app creates `arena.db`
inside that directory. The free, zero-configuration setup remains the default.

## Manual service setup

If you prefer not to use the Blueprint:

1. Create a new **Web Service** from the GitHub repository.
2. Runtime: **Python**.
3. Build command: `pip install --upgrade pip && pip install -r requirements.txt`
4. Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Set `PYTHON_VERSION=3.12.10`, `ARENA_TERRAFORM=0`, and
   `ARENA_ALLOW_APPLY=0`.
6. Optional: set the Google variables listed above and `ARENA_SECRET_KEY`.
7. Health check path: `/api/health`.

## Verify

After the deploy finishes, open the service URL and check:

```text
GET /api/health
```

Expected values include `"ok": true`, `"challenges": 135`, and
`"live": { "apply_enabled": false }`. The health endpoint is also available at
`/health` and `/healthz` after deployment; `/api/health` works on older builds.
