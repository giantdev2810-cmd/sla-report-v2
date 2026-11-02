# Current project state

Updated: 2026-11-02 at T03 attempt 2. The replacement inspection is Awaiting review.
The application and dependency pins are unchanged.

## Current objective and authorization

- W05/W06/W07/W08 and T01/T02 are explicitly accepted. W01/W02/W03 still lack
  recorded explicit acceptance. W08's accepted status and post-merge records are
  carried forward here in the approved T03 restart scope.
- The user requested "hủy T03 và bắt đầu T03 lại". T03 attempt 1 is Canceled;
  PR #3 is closed. Its branch/commits and historical evidence remain intact in
  [the archived record](plan/tasks/T03-attempt-1.md). No raw bodies exist for it.
- The subsequent "duyệt" approves the concrete replacement T03 proposal: preserve
  local context, create a new branch from main, add raw/output/metadata capture
  and offline tests, perform one bounded run, document findings, commit/push/open
  a PR into main. See [T03 attempt 2](plan/tasks/T03.md).
- Attempt 2 completed 11 GETs, all 200, and is Awaiting review. Its budget is
  consumed; no further live call or rerun is authorized. No architecture,
  application change, or PR merge is authorized by this proposal.

## Git and preserved context

- Public repository: giantdev2810-cmd/sla-report-v2; origin is configured.
- Setup PR #1 merged as c601c42; documentation PR #2 as 857bd68; W08 PR #4 as
  ec9927f, including the raw-output rule and ignore entry. Task acceptance is
  distinct from these externally observed merges.
- Prior branch: docs/w08-save-api-inspection-output at 033da4b, with three local
  context-file updates for W08 acceptance/T03 cancellation. The approved named
  stash `preserve W08 acceptance and T03 cancellation` is retained as backup.
- Local main was fast-forwarded to ec9927f, then branch
  `chore/t03-inspect-api-restart` created before edits. Context files were copied
  from the stash; W08 stays Done. No reset, branch deletion, or history rewrite.
- Old script from 693f4d0 was used as the starting point, with new capture support
  and offline tests. Canceled PR #3 was not merged and its branch was not changed.
- Approved commit scope: scripts/inspect_api.py, scripts/tests/test_inspect_api.py,
  docs/plan/tasks/T03.md, T03-attempt-1.md, W08.md, PLAN, STATE, and DECISIONS.
  Message: `chore: restart API inspection with raw capture`. Push the task branch
  and create a PR to main; keep merge approval separate.
- Git delivery: pending. Use live refs and the delivery report for the final hash.

## Current implementation and evidence

- Capture creates a separate ignored local run directory before access. Each
  response body is saved as httpx response.content bytes before status/JSON checks;
  output.jsonl retains sanitized summaries, metadata.jsonl records request time,
  endpoint, safe page/limit parameters, status, and body filename/length. No request
  authorization header is saved; raw response cursors stay outside metadata/output.
- Capture/HTTP/JSON/transport failures stop traversal without retries. A storage
  failure may also prevent saving the final failure record; safe terminal output
  is the fallback. Request ceiling is twelve; redirects are not followed.
- Offline tests: `python -B -m pytest -q scripts/tests/test_inspect_api.py`:
  **11 passed in 0.53s**, before live access. No live traffic in those tests.
- Live run: 2026-11-02 09:33:25.689712 to 09:33:27.824584 UTC (starts 16:33:25
  Vietnam), exit 0, eleven GETs, all 200. Event page 2 skipped for has_more=false.
  Restarting did not reset changes triggered by the earlier first call.
- Private evidence: `.local/inspect/T03/20261102T093325641343Z/`. Eleven .body files
  total 76276 bytes; metadata has eleven rows; sanitized output has 32 rows.
  Offline reconciliation passed: attempts/statuses/final count agree; body sizes
  match metadata; all bodies parse as JSON; all paths ignored; no raw files tracked;
  raw next_cursor strings absent from metadata/output. No additional GETs used.
- Repository checks passed: exact eight-file scope, 26 local links, whitespace,
  Python syntax, statuses, generic credential-pattern scan, preserved backup stash,
  unchanged app/specs/pins/AGENTS/ignore rule, and preserved DECISIONS headings and
  candidate assumption. The pattern scan is not an exhaustive secret audit.
- Observed: 3 sites, 15 staff, 4 statuses; two holiday lists of 5 and 2 rows,
  all DD/MM/YYYY. Third site's holidays untested. Request pages each have 100
  distinct integer IDs, share one ID with identical payloads, and both report
  total=11999, per_page=100, total_pages=122 (ordinary ceiling division gives 120).
  First-page created_at values parse as UTC ISO strings ending Z. Cause of the
  pagination discrepancy and full acquisition remain unverified.
- One detail and its one event: integer at, null actor, local-format due_at,
  no reverting event, has_more=false. Two change pages of five rows accepted
  cursor continuation, each has_more=true, ascending sequences per page; combined
  types: 5 request.created and 5 event.created. Feed not drained; expiry,
  duplicates, current payload semantics, staff changes, and event paging untested.
- DECISIONS preserves the candidate's assumption and four headings; additions
  record supported API observations, AI assistance using write-decisions, and
  the private-sample coverage trade-off. Old findings are not relabeled as new data.

## Application and limits

The active starter is app/ (package app/app/, tests app/tests/, static app/static/).
Health returns 200; ready 503, report/browse 501 by inspection. No SLA calculation,
ingestion, persistence, refresh, cursor browsing, or architecture implemented.
Historical T02 checks passed for pinned packages, local health, Docker build/new
image test, and existing service HTTP health; not repeated for this diagnostic
change. See development.md and T02. New checks do not establish SLA correctness,
readiness, performance, freshness, or browsing guarantees. Raw evidence is local
and not available through the public repository.

## Next action

Finish approved Git delivery and check refs, then obtain explicit acceptance of
T03 attempt 2 and separate PR merge approval. Preserve the canceled first attempt
and W08 backup stash. Do not rerun the script to repopulate context; use the saved
local evidence. T04 still requires its own concrete design proposal and approval.
