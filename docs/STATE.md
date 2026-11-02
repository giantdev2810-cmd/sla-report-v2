# Current project state

Updated: 2026-11-02 after M01 checkpoint publication and the request to document
current status and future priorities. No new runtime verification accompanies this update.
M01 is In progress; final live report verification is blocked by the failed load.
Planning is accepted; T05/W09/T04 are Done. The user now explicitly requested
commit/push of the current M01 checkpoint; PR creation remains gated on acceptance.

## Scope and current behavior

- The user assumes due_at is synchronized with due_on. DECISIONS records this as
  current due_on matching the site-local date of the latest eligible event due_at,
  not all historical deadlines. This is unverified and authorizes no code/fallback
  change: rule 6 continues using the full event deadline, not date-only due_on.
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

- Later manual-check evidence: load 20261102T114645415129Z ended with
  requests_changed after 2283 attempts (2282 HTTP 200, one HTTP 503). Offline
  comparison found 1910 included October IDs in all three walks, no included
  additions/removals, but three request payloads changed between walks 2 and 3:
  updated_at changed in three and status in two. The approved strict reconciliation
  rejected the entire snapshot. This is distinct from the earlier transport failure.
  Another load was observed started at 11:56:40 UTC; do not interrupt or restart it.
  No new agent-driven upstream call was made to diagnose the manual report error.
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
  ignored/untracked evidence, and empty index at the pre-publication checkpoint. Reconciliation found
  1309 metadata attempts across two failed loads and 1303 raw HTTP bodies; all
  HTTP 200 bodies parse as JSON. Transport failures have no invented body/status.
- Local final-image smoke checks: page 200, health 200, ready 503, invalid report
  dates 400; these calls did not trigger upstream acquisition. Stable request
  walks remain a practical check, not an upstream snapshot/completeness guarantee.

## Git and preserved user work

- Branch docs/m01-mvp-plan, based on main 93d77fe (PR #11). The user requested
  "đẩy lên remote đi", explicitly approving this checkpoint commit/push before
  final acceptance. Reuse approved message `feat: deliver level-one SLA report MVP`.
  The 19-file checkpoint was committed and pushed as 8245aef, with local/upstream
  equality verified. The current documentation update is local/uncommitted.
  This request does not accept M01 or authorize a PR/merge. Starter deletions and
  private capture remain excluded; service/runtime is untouched by publication.
- The user's later full-publication request included all 46 starter deletions;
  they are committed in 9e5fb54, together with notes and updated setup references.
- Preserve stashes `preserve T05 delivery records before MVP planning`,
  `preserve T03A deferral records before returning to T04`, and
  `preserve W08 acceptance and T03 cancellation`. Do not apply old PLAN/STATE over
  the current plan. T03A remains deferred. Private T03/M01 capture is never public.
- W05/W06/W07/W08/W09 and T01/T02/T03 attempt 2/T04/T05 are accepted; W01/W02/W03
  still lack recorded acceptance. M02–M04 are not approved for implementation.

## Next action

The reviewer-facing future-work priorities are recorded in DECISIONS: finish
real-data level 1 verification, investigate completeness, measure/extend six-month
loading, then add live updates and browsing. These are future plans, not approval
to implement them or rerun the API. M01 remains unaccepted and no PR was created.

Offline scope/evidence checks are complete; await manual feedback. A new bounded
agent-driven live session needs explicit approval because the one approved session
ended unsuccessfully; do not silently retry. Preserve user deletions/stashes, keep
M01 In progress, and report the live verification limit honestly. Previous elapsed
assignment time is unmeasured; do not claim compliance with the three-hour cap.


## Latest publication authorization

The user requested "đẩy toàn bộ lên github và tạo PR", explicitly authorizing
publication of all current tracked/unignored work, including their 46 starter
file deletions, and creation of a PR before final M01 acceptance. This supersedes
the earlier exclusion/PR timing only for this checkpoint; it does not accept M01,
authorize merging, publish ignored credentials/capture, or resume API verification.
The user supplied a 200 access log for 1 October 2026; treat that as user-reported
HTTP success for one day, not independent full-month or SLA correctness evidence.
Keep stashes/private evidence. Use live branch/PR refs for publication results.

Full publication commit 9e5fb54 was pushed. PR
[#12](https://github.com/giantdev2810-cmd/sla-report-v2/pull/12) targets main from
docs/m01-mvp-plan. This delivery record is a checkpoint on the same branch;
use live refs for its final tip. No merge or new live verification was performed.
