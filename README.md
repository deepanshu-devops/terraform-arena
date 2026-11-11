# Terraform Arena

A local, HackerRank-style practice platform for Terraform / Infrastructure-as-Code.
Write HCL in VS Code or the built-in editor, run your own tests, and get a
structured verdict:

```
[PASS] / [FAIL]
  per-test results       (syntax, resources, security, lifecycle, outputs, variables)
  architecture drift
  formatting grade       (terraform fmt conventions)
  variable compliance    (declared / typed / defaulted / used)
  security policy        (allowlist, no shell provisioners, no hardcoded creds)
```

Everything runs offline. No AWS calls are made by default.

---

## Contents

| | |
| --- | --- |
| Challenges | **117** (7 level-0 intros + 105 catalog scenarios + 5 capstones) |
| Progression | Level 0 (HCL basics) through level 5 (capstones) |
| Physical workspaces | `workspaces/001-...` through `workspaces/117-...` |
| Backend | Python 3.12 + FastAPI + SQLite |
| Queue | ThreadPoolExecutor + `jobs` table (Celery/Redis-shaped) |
| Evaluation | Custom HCL lexer/parser + rule engine |
| Frontend | Vanilla HTML/CSS/JS, dark HackerRank-style UI |
| Cloud cost | $0 (static analysis; optional Terraform CLI) |

---

## Quick start

```powershell
cd terraform-arena
.\run.ps1
```

Then open <http://127.0.0.1:8000>.

Manual start:

```powershell
python -m pip install -r requirements.txt
python judge.py generate
python -m uvicorn app.main:app --reload --port 8000
```

---

## How a challenge works

Every scenario is authored as a complete, working Terraform configuration.
The learner receives all of that surrounding code with **exactly one focused
block replaced by an in-place TODO** - the LeetCode model applied to IaC.

- The block header stays visible (the "function signature").
- Only the body of the focus block is missing.
- The folder README names the file and task; `challenge.json` carries the same
  focus metadata.
- Hidden assertions are revealed only after a submission.

This keeps the exercise about one concept at a time: fill the block, run the
tests, and the complete configuration around it should snap into place.

One deliberate exception is the level-0 formatting drill: it gives you working
code in bad style and asks you to reformat it instead of filling a TODO.

---

## VS Code workflow (recommended)

1. Generate / refresh workspaces:

   ```powershell
   python judge.py generate
   ```

2. Browse the catalog:

   ```powershell
   python judge.py list
   python judge.py list --level 0
   python judge.py list --difficulty Hard
   python judge.py list --tag s3 --search encryption
   ```

3. Show a challenge statement (number or stable id):

   ```powershell
   python judge.py show intro-hcl-blocks
   python judge.py show 61
   ```

4. Open the matching folder in VS Code, e.g.
   `workspaces/061-provision-vpc/`. Each folder contains:

   ```
   versions.tf   variables.tf   main.tf   outputs.tf   README.md   challenge.json
   ```

   The surrounding configuration is complete. Find the single
   `# TODO - ...` block inside the focus file and complete it.

5. Fill in the TODO and run:

   ```powershell
   python judge.py test 61
   ```

   Or test every workspace you have touched:

   ```powershell
   python judge.py test-all
   ```

6. If the catalog changes and you want refreshed starters without losing work:

   ```powershell
   python judge.py refresh-starters
   ```

   A file is refreshed only when it is comment-only or still matches the starter
   snapshot in its `challenge.json`. Files you have edited are preserved. Use
   `--force` only when you intentionally want to overwrite learner code.

Exit code is `0` on PASS, `1` on FAIL, so it works in CI too.

---

## Progression and catalog

The catalog is sorted by level, then points, then title. Numbering starts at 1.

| Level | Name | Range | Focus |
| --- | --- | --- | --- |
| 0 | HCL Foundations | `001`-`007` | blocks, arguments, strings, formatting, collections, providers, file layout |
| 1 | Terraform Language | `008`-`017` | variables, validation, locals, count, for_each, conditionals, data sources, lifecycle, depends_on |
| 2 | First Resources | `018`-`063` | one resource at a time: S3, VPC, EC2, RDS, DynamoDB, Lambda, IAM, Docker and more |
| 3 | Real Infrastructure | `064`-`086` | encryption, TLS, retention, IMDSv2, least privilege, public-access lockdown |
| 4 | Composition | `087`-`106` | multi-resource wiring: ALB, Lambda, ECS, RDS, DNS, KMS, messaging, observability |
| 5 | Modules & Capstones | `107`-`117` | modules, state, refactoring, import, plus the five full-capstone builds |

Themes recur across levels: S3 security, VPC design, EC2 hardening, RDS,
DynamoDB, Lambda, API Gateway, IAM least privilege, KMS, messaging,
observability, modules, remote state, refactoring and Docker.

Open `workspaces/INDEX.md` for the full table with each focus block.

### Capstones

| # | Challenge | Difficulty |
| --- | --- | --- |
| 112 | Docker Nginx Sandbox | Easy |
| 114 | Secure S3 Bucket Provisioning | Easy |
| 115 | Highly Available VPC Foundation | Medium |
| 116 | Auto Scaling Web Tier | Hard |
| 117 | Serverless Item API | Hard |

Each capstone supplies every supporting file and masks one central resource
body (bucket, container, subnet, Auto Scaling group, or Lambda function).

---

## How grading works

1. **Syntax gate** - the custom HCL parser checks brace balance, unterminated
   strings, duplicate attributes, heredocs, etc.
2. **Hidden tests** - each challenge has a test manifest. Tests are only
   revealed *after* a submission. The public statement exposes categories and
   points but not the assertions.
3. **Security policy** - blocks expensive/identity resources, wildcard IAM,
   `local-exec`/`remote-exec`, non-free-tier instance types, runaway loops,
   hardcoded credentials and resources outside the challenge allowlist.
4. **Drift detection** - missing expected resources and unexpected resources
   outside scope.
5. **Formatting grade** - tabs, trailing whitespace, CRLF, indentation,
   long lines, final newline.
6. **Variable compliance** - every documented variable must be declared with
   the right type/default/validation and actually referenced.

The result is `PASS` only when the syntax is clean, every required test passes,
and the security policy is not violated.

`python judge.py verify` is the developer gate: it checks that all 117 reference
solutions pass, every masked starter fails, starters parse cleanly, and focus
markers never leak into learner files.

---

## Architecture

The default workflow is offline and static: no AWS calls, no cloud spend. The
submission path is already asynchronous (API -> `jobs` row -> worker ->
persisted `test_results`), so the grading backend can be scaled out without
changing the UI.

For the production blueprint - queue, Docker workers, `terraform validate`,
sandbox apply/destroy, Trivy/TFSec and the SQLite -> Postgres migration path -
see [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md).

---

## Optional: real Terraform CLI

The platform ships with a zero-dependency static engine. To also run
`terraform init -backend=false` + `terraform validate`:

```powershell
powershell -ExecutionPolicy Bypass -File scripts\install_terraform.ps1
$env:Path = "$PWD\tools\terraform;$env:Path"
$env:ARENA_TERRAFORM = "1"
.\run.ps1
```

Live `apply`/`destroy` is disabled by default. The explicitly gated AWS pilot
is separate from the app and runs only through `judge.py live`:

```powershell
python judge.py live --status
python judge.py live provision-vpc                 # plan only; creates nothing
$env:ARENA_LIVE_APPLY = "1"
python judge.py live provision-vpc --apply --yes   # apply + destroy in a sandbox account
```

It requires a dedicated sandbox account, a local AWS profile, an account-id
allowlist, a plan-JSON resource allowlist, and explicit `--apply --yes`.
The pilot allowlist is keyed by stable challenge id, so renumbering the catalog
cannot silently change what may run live.
See [`docs/LIVE_AWS.md`](docs/LIVE_AWS.md) for the full safety policy and
cleanup procedure.

No AWS resources are ever created by the default workflow.

---

## API

| Method | Path | Purpose |
| --- | --- | --- |
| GET | `/api/health` | health + Terraform status |
| GET | `/api/stats` | solved/attempted/submissions/average |
| GET | `/api/challenges` | catalog with filters (`level`, `difficulty`, `tag`, `search`) |
| GET | `/api/challenges/{number-or-id}` | public challenge statement + focus block |
| POST | `/api/submit` | `{ "challenge": "61", "files": {...} }` -> job id |
| GET | `/api/jobs/{id}` | poll job state + result |
| GET | `/api/submissions` | recent submissions |
| GET | `/api/submissions/{id}` | full result |
| GET | `/api/progress` | per-challenge progress |
| GET | `/api/terraform/status` | CLI detection |

Interactive docs: <http://127.0.0.1:8000/docs>.

---

## Layout

```
terraform-arena/
  app/
    hcl.py            HCL lexer/parser
    checks.py         reusable assertions
    evaluator.py      test runner, security policy, grading, drift
    declarative.py    spec -> Challenge compiler
    catalog/
      intro.py        level-0 HCL fundamentals
      specs.py        provision resource blueprints
      extra.py        hardening, wiring, language, module, Docker specs
      reference.py    reference synthesis, focus selection, masking
      __init__.py     catalog loader + README rendering
    challenges/       hand-authored capstones + registry
      solutions.py    complete capstone references and focus metadata
    db.py             SQLite schema + CRUD
    jobs.py           async evaluation queue
    runner.py         optional Terraform CLI integration
    workspace.py      workspace export helpers + safe starter refresh
    main.py           FastAPI app
  static/             HackerRank-style UI
  workspaces/         117 folders of incomplete .tf files
  scripts/            workspace generator + Terraform installer + ref checks
  docs/               architecture blueprint + API notes
  judge.py            local CLI (list/show/start/test/test-all/verify/live)
  run.ps1             one-command launcher
```

---

## Adding challenges

Add a resource tuple to `app/catalog/specs.py` (`RESOURCES`), a spec to one of
the lists in `app/catalog/extra.py`, or a hand-authored intro to
`app/catalog/intro.py`. Then:

```powershell
python judge.py verify
python judge.py generate
```

Specs use declarative checks (`resource_exists`, `attr_ref`, `tagged`,
`nested_path`, `no_wildcard_iam`, ...) so a new scenario rarely needs Python.
The reference generator synthesises a complete solution from those checks and
masks exactly one focus region for the starter. `verify` must stay green before
workspaces are regenerated.
