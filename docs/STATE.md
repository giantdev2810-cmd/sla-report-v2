# Current project state

Updated: 2026-11-02 at the W08 checkpoint. W08 is Awaiting review and changes
workflow documentation plus an ignore rule only. Application code is unchanged.

## Current objective and authorization

- W05/W06/W07 and T01/T02 are explicitly accepted. W01/W02/W03 still lack recorded
  explicit acceptance. T03 is Awaiting review in its separate PR; its acceptance
  and merge are not authorized by the W08 approval.
- The user requested saved inspect output, clarified "lưu output raw luôn", then
  replied "duyệt" to the revised W08 proposal. Approved files: `.gitignore`,
  AGENTS, PLAN, STATE, and `plan/tasks/W08.md`.
- W08 requires future approved inspections to save unchanged response bodies,
  including error responses, plus sanitized output and request metadata at
  `.local/inspect/<task-id>/<UTC-timestamp>/`. Create the directory before access;
  stop further requests if evidence cannot be saved. No authorization headers or
  configured tokens are recorded; response-body cursors stay only in raw local files.
- No script implementation, additional API request, reconstruction of T03 output,
  or merge is authorized. Existing summary-only inspection tools need approved
  capture support before another live inspection. See [W08](plan/tasks/W08.md).

## Git and branch boundaries

- Public repository: `giantdev2810-cmd/sla-report-v2`; origin is configured.
- Setup PR #1 merged as `c601c42`. Documentation commit `7d84cb1` was published
  on feat/sla-report, then PR #2 merged into main at `857bd68`.
- T03's implementation/evidence commit is `72651b1`; its delivery-record checkpoint
  is `693f4d0`. Both remain on `chore/t03-inspect-practice-api` in
  [PR #3](https://github.com/giantdev2810-cmd/sla-report-v2/pull/3), observed OPEN
  during W08 preparation. T03's script and record are not present on this base.
- Working tree was clean before W08. After fetching, main was already up to date
  at `857bd68`; branch `docs/w08-save-api-inspection-output` was created from it
  before edits. T03 was neither merged nor modified.
- Approved W08 delivery: commit the five-file scope with message
  `docs: require saved API inspection output`, push this branch, and open a PR to
  main. The task record and delivery report hold the resulting commit/PR evidence;
  check live refs for the final checkpoint hash and tracking state.

## Implementation and historical evidence

- Active application: app/, Python package app/app/, tests app/tests/, page
  app/static/. Starter health returns 200; ready returns 503 and report/browse
  return 501 by inspection. No SLA calculation, storage, ingestion, refresh,
  cursor browsing, or architecture has been implemented/selected.
- T02 installed the unchanged exact pins with compatible packages. Historical
  health results: local 1 passed in 1.46s; temporary Docker container/new image
  1 passed in 0.48s; existing service HTTP health 200. Build succeeded; existing
  service was preserved. These checks were not rerun for W08. See
  [development](development.md) and [T02](plan/tasks/T02.md).
- T03's prior live run completed 11 GETs, all 200, starting at 09:10:30.690 UTC
  (16:10:30 Vietnam time). Raw bodies were not retained. Its summary reported one
  shared ID across two request pages and inconsistent total/page-count arithmetic;
  one event and two small change-feed pages leave broad coverage unverified.
  Full evidence remains in PR #3; do not call the API to repopulate context.
- W08 did not call the practice API, read private configuration, create raw-output
  files, or change scripts, specifications, dependencies, or DECISIONS. No new
  API/design finding warrants a DECISIONS entry for this workflow-only change.
- Raw files are local and ignored. The public task record identifies their local
  directory only when an actual inspection creates it; W08 has no such run path.

## Verification and limits

W08 checks passed: exact five-file scope, 18 local links, whitespace/diff check,
task/index status agreement, and generic credential-pattern scan. Raw/output/
metadata sample paths are ignored; the sibling path and task record are not.
No raw files are tracked or were created. Code, specs, and DECISIONS are unchanged.
These checks establish workflow guidance and ignore matching,
not that any script actually captures responses. W08 does not establish SLA
correctness, readiness, performance, refresh, or pagination guarantees.

## Next action

Complete the approved W08 commit/push/PR delivery, then obtain explicit candidate
acceptance and separate merge approval. Keep T03 review/merge decisions separate.
Any change to the inspection script or new live request budget needs a concrete
proposal and approval. Do not regenerate missing T03 raw responses.
