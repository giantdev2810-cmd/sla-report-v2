# Development environment

The active application is `app/`, copied unchanged from the supplied Python/FastAPI starter. Docker uses Python 3.12; `.python-version` selects the same version locally. The original starter folders are kept as references.

## Docker (submission runtime)

Start Docker Desktop with its Linux engine, then run from the repository root:

```powershell
docker compose up --build -d
docker compose run --rm app test
Invoke-RestMethod http://localhost:8080/health
```

Open http://localhost:8080. Health should return `{"ok": true}`.

The root `.env` contains `HELPDESK_URL` and `HELPDESK_TOKEN`. Compose passes them to the container. If it is missing, copy `.env.example` to `.env` and fill in the invitation credentials privately. Never commit `.env` or `Requirements.md`; both are ignored because the invitation contains the API token. Do not include them in the submission archive.

## Local Windows development

With Python 3.12 and uv installed, run from the repository root:

```powershell
uv --cache-dir .uv-cache venv --python 3.12 .venv
uv --cache-dir .uv-cache pip install --python .venv\Scripts\python.exe -r app\requirements.txt
uv pip check --python .venv\Scripts\python.exe
.\scripts\dev.ps1 test
.\scripts\dev.ps1 start
```

The start command loads the two helpdesk variables from the root `.env` and starts uvicorn with reload at http://localhost:8080. The test command runs pytest from the application folder. No virtual environment activation is required.

Run and test through Docker before submission even when developing locally. Dependency versions remain exactly as supplied in `app/requirements.txt`.

## Current setup verification

Checked on 2026-11-02 in T01/T02:

- Python in `.venv/` is `3.12.13`. uv `0.12.2` installed all six direct dependencies at the exact supplied versions, plus their transitive dependencies. `uv pip check` passed.
- `scripts/dev.ps1 test` passed: `1 passed in 1.46s`.
- Docker CLI and Engine `29.9.2` and Compose `v5.6.1` are available. `docker compose config --quiet` passed in T01.
- `docker compose build app` succeeded. `docker compose run --rm --no-deps app test` tested the new image in a temporary container: `1 passed in 0.48s`.
- The existing app container on port 8080 was preserved. GET `/health` returned HTTP 200 with `{"ok": true}`. This HTTP result applies to that existing container; the temporary-container test validates the new image.
- Earlier dependency-download and Docker-Engine failures no longer block these commands. Private-file ignore rules were verified earlier, not rescanned in T02.
- No practice API calls were made by the agent during setup or T01/T02. Health checks do not establish SLA report correctness or six-month readiness.

When an app container is already running, the build/test commands above validate a new image without replacing that service. Applying the new image to the running service is a separate action.

## Starter behavior

Only the starter is configured so far. `/health` returns 200; `/ready` intentionally returns 503, and the report and browse endpoints return 501 until implemented. Starting this starter does not contact the practice API.
