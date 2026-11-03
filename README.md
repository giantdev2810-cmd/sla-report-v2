# Response-time SLA report

A Python 3.12 / FastAPI application that calculates helpdesk response-time SLA
reports and responder totals. The page uses plain HTML, CSS and JavaScript;
HTTPX retrieves upstream data, and a single application worker keeps the last
successful data snapshot in memory. No database is required.

The level-one report path is implemented. Full live-data correctness and coverage
remain unverified; six-month readiness/performance, live updates and browsing
are unfinished. See [DECISIONS.md](DECISIONS.md) for assumptions, API findings,
AI assistance and trade-offs.

## Setup

You need Git and Docker with Compose, using Linux containers. Run the following
from the root of a cloned repository.

1. Copy `.env.example` to `.env` (`cp .env.example .env` in a POSIX shell,
   or `Copy-Item .env.example .env` in PowerShell).
2. Set `HELPDESK_URL` and `HELPDESK_TOKEN` in `.env` to the supplied API details.
3. Build and start the app:

```bash
docker compose up --build
```

Open <http://localhost:8080>, select **From** and **To**, and click **Run report**.
For a single day, select the same date in both fields. The first report loads
upstream data synchronously and may take several minutes. The page shows loading,
error or result states; it does not stream partial rows.

Health check, in another terminal:

```bash
curl http://localhost:8080/health
```

Expected health response: `200 {"ok": true}`. Health does not establish report
readiness or correctness. The Compose service is named `app`, listens on port
`8080`, and reads `HELPDESK_URL` and `HELPDESK_TOKEN` from the environment.

Keep `.env`, the private invitation `Requirements.md` and `.local/inspect/`
captures out of public repositories and submission archives.

## Tests

Run the test suite in Docker:

```bash
docker compose run --rm app test
```

Exit code zero means the tests passed. The suite uses synthetic inputs and mock
HTTP responses to check SLA rules, aggregation, acquisition, API behavior and
capture. It does not prove correctness or completeness on the grading dataset.

For local Windows setup and commands, see [docs/development.md](docs/development.md).
Docker is the grading runtime; check the build before submitting.

## Endpoints and report behavior

| Endpoint | Current behavior |
| --- | --- |
| `GET /` | Date selection, request rows and responder totals |
| `GET /health` | `200 {"ok": true}` |
| `GET /ready` | `503 {"ready": false}`; six-month readiness is unfinished |
| `GET /api/sla-report?from=YYYY-MM-DD&to=YYYY-MM-DD` | SLA report for the inclusive site-local creation-date range |
| `GET /api/requests` | `501`; level-four browsing is unfinished |

For example, selecting 12 October 2026 in both date fields sends
`GET /api/sla-report?from=2026-10-12&to=2026-10-12` and, on success, displays
the response's `requests` and `responders` arrays. Requests that are canceled,
deleted or merged are excluded. The report uses the acquired event histories
for response/completion rules and the current staff names.

The page displays JSON `null` as `—`. Under rule 7, no eligible first response
means responder and response metrics are null; no eligible completion or no
deadline means completed-late is null. Nonconsecutive IDs alone do not demonstrate
missing records. The reported blank/null rows have not been individually verified.

Missing, invalid, duplicate or reversed dates return `400`. Malformed or
conflicting acquired data returns `502`; transport, budget or unusable-load
failures return `503`. Detected acquisition inconsistencies fail the load rather
than publish its partial result. Exact shapes and business rules are in the
[contract](docs/contract.md) and [rules](docs/rules.md).

## Known limitations

- Acquisition scans request pages three times and loads the needed per-request
  event pages sequentially. Changing request data can cause the reconciliation
  check to reject a load. Agreeing walks do not prove complete upstream coverage
  or a transactionally consistent snapshot.
- Loads are capped at 6000 upstream attempts and thirty minutes, with bounded
  retries and rate pacing. These limits are not the level-two performance targets;
  those targets have not been demonstrated.
- The last successful range is cached in process-local memory. Repeating that
  range or a subrange reuses its snapshot without refreshing upstream data.
  Another range outside cached coverage requires a new load; restart loses the
  cache. There is no automatic live refresh or shared multi-worker store.
- Six-month readiness, live updates within 60 seconds and browse filters,
  sorting and cursor pagination remain unfinished. Report code and offline tests
  are not a claim that any grading level has been independently verified.

## Code and reference documents

- `app/app/`: HTTP endpoints, upstream client, acquisition, snapshot store and
  pure SLA/report calculations.
- `app/tests/`: offline tests; `app/static/index.html`: the report page.
- [docs/api.md](docs/api.md): documented upstream endpoints and fields.
- [docs/architecture.md](docs/architecture.md): module responsibilities and data flow.
- [DECISIONS.md](DECISIONS.md): rationale, findings, AI use and future work.

The original submission instructions follow.

## Submitting

1. Commit as you go (at least 5 commits); we read the history.
2. Fill in `DECISIONS.md`.
3. Record a short screen recording (about 3 minutes) of the app, narrated in English.
4. Push to a **public** repo (e.g. GitHub) and paste the link on your invitation page, or zip the
   folder **including `.git`** (leave out `node_modules` and `.env`) and upload it there.

Cap it at 3 hours. Go through the levels in order and say in `DECISIONS.md` what you'd do next.
**Submit even if it's unfinished:** we review everything you did, not only the final result.
A plain table is enough; polish isn't scored. We never reuse submissions as company work.
