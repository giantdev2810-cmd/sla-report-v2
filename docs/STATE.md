# Current project state

Updated: 2026-11-02 after explicit T05 acceptance.
T05, W09 and T04 are Done. Approved T05 Git delivery is next.

## Current scope and authorization

- The user confirmed the reversal-chain interpretation, requested recording it in
  DECISIONS assumptions, then explicitly approved the full proposal with
  "duyệt t05". This approves implementation, not acceptance of the result.
- After the review handoff, the user stated "tôi là người xóa chúng, chấp nhận t05",
  explicitly accepting T05 and confirming ownership of the starter deletions.
  The approved seven-file Git delivery gate is now satisfied; merge remains separate.
- [T05](plan/tasks/T05.md) covers seven files: app/app/sla.py,
  app/tests/test_sla_events.py, T05 record, PLAN, STATE, architecture, DECISIONS.
  It implements only the pure rule-2 filter; no API access, dependency change,
  endpoint wiring, schema validation, deduplication, or remaining SLA calculation.
- eligible_events takes valid id/reverts_id event dictionaries for one request,
  collects every non-null referenced ID, and excludes both referencing events
  and referenced IDs. It returns a new list preserving retained dictionaries/order
  without mutating input. Two passes and a set cost O(n) time and O(n) space.
- Approved assumption: B reverts A and C reverts B excludes all three, with no
  restoration of A. An absent target does not make its reverting event eligible;
  this does not establish history completeness. DECISIONS retains this assumption.
- After candidate review and explicit acceptance, commit/push and PR may proceed
  with approved scope/message; no draft PR before acceptance. Merge is separate.
  T06 needs its own proposal; T03A stays deferred.

## Git and preserved work

- Current branch: feat/t05-exclude-reverted-events, created from updated main
  124e14a (PR #10 observed merged) before the assumption-only edit. Full T05
  approval includes the existing local DECISIONS/STATE edits.
- Approved message: `feat: exclude reverted and reverting events`.
  Publish only the accepted seven-file scope; actual commit/PR pending delivery. No reset,
  branch deletion, history rewrite, or merge was performed.
- During validation, 46 unrelated files under starters/ appeared as deleted. The
  user confirmed these intentional deletions are theirs. Leave them untouched and exclude them from
  T05 staging/delivery. The initial whole-tree scope assertion failed on those
  deletions, then validation of the seven approved T05 files passed.
- W09 roadmap/dependencies and T03A record are now in main. PR #9 merged as
  9c207c0, PR #10 as 124e14a; agent merges were not authorized or performed.
- Preserve stashes `preserve T03A deferral records before returning to T04` and
  `preserve W08 acceptance and T03 cancellation`, canceled T03 history, and private
  captures. T03A remains Approved — deferred by user with no tool implementation.
- W05/W06/W07/W08/W09 and T01/T02/T03 attempt 2/T04/T05 are explicitly accepted.
  W01/W02/W03 still lack recorded explicit acceptance.

## Implementation and evidence

- app/app/sla.py now implements only eligible_events. The report, responder,
  business-hours, ingestion, store, refresh and browsing paths remain future work.
  Starter endpoints are unchanged: health 200, ready 503, report/browse 501 by
  inspection. The existing health test also passes in the current run.
- From app/, `..\.venv\Scripts\python.exe -B -m pytest -q`:
  **11 passed in 0.77s**, ten rule-2 cases plus health. Tests cover pair order,
  multiple/shared targets, no restoration through chains, absent targets, zero
  versus null, empty/no-reversal input, new list, non-mutation and retained payloads.
  Fixtures are synthetic; no network/ingestion path or full report was validated.
- Scoped checks passed: seven approved T05 files, 36 local links, Python syntax,
  DECISIONS headings/assumptions, review statuses, both stashes, ignored/untracked
  captures, scoped whitespace, and generic credential scan. At the pre-review
  checkpoint HEAD was 124e14a with empty index. Starter deletions remain outside scope.
- [Architecture](architecture.md) still uses request/event baseline loading,
  references, feed updates, process-local memory with one worker, and report
  snapshots. It now identifies rule 2 as implemented and all other work as pending.
  Open ingestion, concurrency, timestamp tie and recovery questions remain open.
- T03's only replacement live run was eleven GETs, all 200; prior capture tests
  and W09 documentation checks are historical. The T03 request budget is consumed.
  Private capture `.local/inspect/T03/20261102T093325641343Z/` retains eleven raw
  bodies totaling 76276 bytes and readable copies. All stay local/ignored;
  do not publish raw cursors or payloads. No extra API run is authorized.
- T05 tests do not establish other SLA rules, complete data, readiness, speed,
  freshness, browsing correctness, or current container behavior.

## Next action

Publish accepted T05 through its approved seven-file commit/push/PR and record
delivery. Preserve the user's starter deletions outside T05. Merge needs separate
approval. T06 and later tasks need separate proposals. Actual total
assignment time against the three-hour budget has not been measured.
