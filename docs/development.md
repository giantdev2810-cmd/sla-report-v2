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
.\scripts\dev.ps1 test
.\scripts\dev.ps1 start
```

The start command loads the two helpdesk variables from the root `.env` and starts uvicorn with reload at http://localhost:8080. The test command runs pytest from the application folder. No virtual environment activation is required.

Run and test through Docker before submission even when developing locally. Dependency versions remain exactly as supplied in `app/requirements.txt`.

## Current setup verification

- Git is initialized and already contains the starter commit.
- Python 3.12.13 virtual environment created at `.venv/`.
- Docker Compose configuration validated with `docker compose config --quiet`.
- Git ignore rules verified for both private files.
- Python source files compile successfully. The local helper parses and invokes Python correctly; running tests currently exits with `No module named pytest` because dependencies could not be installed.
- Runtime tests and Docker build are pending: Docker Engine was unavailable and Docker Desktop startup reported access denied writing its host log. Dependency installation could not reach PyPI through the current network connection. The local cache does not contain all required versions.
- No practice API calls were made during setup.

## Starter behavior

Only the starter is configured so far. `/health` returns 200; `/ready` intentionally returns 503, and the report and browse endpoints return 501 until implemented. Starting this starter does not contact the practice API.
