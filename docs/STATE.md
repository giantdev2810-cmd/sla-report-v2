# Current project state

Updated: 2026-11-02 during approved M01 implementation/manual checking.
M01 is In progress; final live report verification is blocked by the failed load.
Planning is accepted; T05/W09/T04 are Done. The user now explicitly requested
commit/push of the current M01 checkpoint; PR creation remains gated on acceptance.

## Scope and current behavior

- The user approved grouping and then the concrete M01 implementation proposal
  with "duyệt". Scope/policies/budget are in [M01](plan/tasks/M01.md). Approval is
  not final acceptance. All three checkpoints now have code: pure SLA/report,
  bounded acquisition/store/capture, and date-validated endpoint plus table UI.
- Sources: app/app/{sla,report,store,ingestion,helpdesk,main,capture}.py; five new
  test files, app/static/index.html; PLAN, architecture, STATE, M01, development,
  DECISIONS. Dependency pins, supplied specs and tracked Compose remain unchanged.
- One worker; sequential HTTP; at least 250 ms between starts; at most three
  attempts per GET, 6000 attempts/thirty minutes per load. Three request walks,
  full required event pages, no partial publication, atomic copied snapshots and
  subrange caching. No automatic refresh or browsing implementation.
- Site-local calendar arithmetic uses UTC elapsed seconds and unions overnight
  windows after holiday splitting. Equal at uses ID order; ambiguous/nonexistent
  local wall times fail. These interpretations are recorded in DECISIONS.
- 400 invalid dates; 502 malformed/conflicting upstream data; 503 unusable or
  failed acquisition. Health is 200; ready stays 503 pending six-month validation.
  The first report may take minutes. Actual app source is app/, not deleted starters.

## Current validation and service

- Final local tests from app/: 53 passed in 1.00s. Final Docker build and container
  suite: 53 passed in 0.76s. All are offline/mock/expected-value checks, not proof
  of full data correctness. An initial root-directory test invocation failed imports
  and was corrected; earlier 51-pass image was used for the live attempt.
- Final tested image is running at http://localhost:8080 using the private capture
  override under `.local/inspect/M01/20261102T113313160223Z/`. It was applied only
  after verifying no active load; no new report/upstream request accompanied it.
- Authorized live session started 11:33:25 UTC and ended 11:39:12 UTC. October
  failed after 346.891s with 503 upstream_transport. Week query skipped; no report
  snapshot was published. Capture has 1306 attempts: 1301 HTTP 200, two HTTP 503,
  three transport failures; 1303 unchanged response bodies and safe metadata/output.
- A second observed load had three ConnectError attempts/no bodies. The verification
  script did not issue it. DNS and TCP later succeeded, but no further agent GET
  or full rerun is authorized by the completed single live session.
- Computer Use stopped because it could not confidently identify Chrome's URL.
  The user said "tôi kiểm tra thủ công". Do not resume browser automation or claim
  visual/manual success. Await their feedback; report success on real data remains
  unverified. Do not mark M01 Awaiting review/Done as a fully verified MVP yet.
- Final scoped checks passed: 19 approved files, 39 local links, Python syntax,
  UTF-8/whitespace, DECISIONS headings/assumption, 46 preserved starter deletions,
  ignored/untracked evidence, empty index and no publication. Reconciliation found
  1309 metadata attempts across two failed loads and 1303 raw HTTP bodies; all
  HTTP 200 bodies parse as JSON. Transport failures have no invented body/status.
- Local final-image smoke checks: page 200, health 200, ready 503, invalid report
  dates 400; these calls did not trigger upstream acquisition. Stable request
  walks remain a practical check, not an upstream snapshot/completeness guarantee.

## Git and preserved user work

- Branch docs/m01-mvp-plan, based on main 93d77fe (PR #11). The user requested
  "đẩy lên remote đi", explicitly approving this checkpoint commit/push before
  final acceptance. Reuse approved message `feat: deliver level-one SLA report MVP`.
  Publish only the 19 M01 files; use live HEAD/upstream refs for the resulting hash.
  This request does not accept M01 or authorize a PR/merge. Starter deletions and
  private capture remain excluded; service/runtime is untouched by publication.
- All 46 user-authored starter deletions remain unstaged, outside M01 scope.
- Preserve stashes `preserve T05 delivery records before MVP planning`,
  `preserve T03A deferral records before returning to T04`, and
  `preserve W08 acceptance and T03 cancellation`. Do not apply old PLAN/STATE over
  the current plan. T03A remains deferred. Private T03/M01 capture is never public.
- W05/W06/W07/W08/W09 and T01/T02/T03 attempt 2/T04/T05 are accepted; W01/W02/W03
  still lack recorded acceptance. M02–M04 are not approved for implementation.

## Next action

Offline scope/evidence checks are complete; await manual feedback. A new bounded
agent-driven live session needs explicit approval because the one approved session
ended unsuccessfully; do not silently retry. Preserve user deletions/stashes, keep
M01 In progress, and report the live verification limit honestly. Previous elapsed
assignment time is unmeasured; do not claim compliance with the three-hour cap.
