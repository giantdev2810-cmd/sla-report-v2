# Current project state

Updated: 2026-11-02 after explicit review and acceptance of the T04 revision.
T04 is Done. Application behavior and dependency pins are unchanged.

## Current scope and review gate

- The user approved the revised T04 proposal with "duyệt" after requesting a new
  proposal plus a PR-after-review rule. Scope: AGENTS, architecture, DECISIONS,
  PLAN, STATE, and T04 record. Approval to revise is not acceptance of the result.
- The user then reported "đã review" and explicitly replied "chấp nhận" after
  clarification. T04's completed documentation is accepted; approved Git delivery
  may now proceed. This does not approve application implementation or merging.
- [Architecture](architecture.md): baseline requests plus full event pages;
  separate sites/holidays/current staff; feed updates; identity-based memory store,
  one worker; pure rules and a consistent report snapshot. These are design choices,
  not implemented behavior. The original feed-only bootstrap is superseded.
- The user confirmed feed history is incomplete and explicitly left other questions
  open: pagination completeness, bootstrap/feed consistency, rate limits/performance,
  version conflicts, event timestamp ties, upstream date-filter timezone, missing
  references, and recovery. Do not silently select policies for these questions.
- Current rule: complete work/checks, explain it, and keep Awaiting review. Only
  after candidate review and explicit acceptance may a PR be created, including
  a draft PR. Commit/push timing follows the approved proposal; merge is separate.
  This applies to active, future, and resumed tasks, including deferred T03A.
- No application changes, dependencies, live API calls, or next-task implementation
  are authorized by T04.

## Git and preserved work

- Current branch: docs/t04-initial-architecture; original base f782423 (merged PR #6).
  Existing design/checkpoint commits f222c39 and 7667ed2 remain on the branch.
- PR [#7](https://github.com/giantdev2810-cmd/sla-report-v2/pull/7) is CLOSED at the
  user's request. Keep it closed. No reset, branch deletion, or history rewrite.
- Approved message: `docs: revise SLA design and PR review workflow`. Candidate
  review and acceptance were recorded before delivery. Revision commit 86d7a9c
  was pushed and PR [#9](https://github.com/giantdev2810-cmd/sla-report-v2/pull/9)
  opened into main. This delivery checkpoint uses the same approved message;
  use live refs for its final tip. No merge was authorized or run.
- T03A is deferred by "task này để sau đi". Only feat/t03a-api-audit was created
  from main; no audit tool, test, live call, or PR. Its local records are preserved
  in stash `preserve T03A deferral records before returning to T04`; do not drop it.
- Preserve the canceled T03 branch/history and stash
  `preserve W08 acceptance and T03 cancellation`.
- W05/W06/W07/W08 and T01/T02/T03 attempt 2/T04 are explicitly accepted.
  W01/W02/W03 still lack recorded explicit acceptance. Merges do not accept tasks.

## Implementation and validation evidence

- Active starter is app/ (package app/app/, tests app/tests/, page app/static/).
  By inspection health returns 200, ready 503, report/browse 501. No ingestion,
  store, SLA calculation, live refresh, or browsing implementation exists.
- T02 historical checks passed: compatible pinned packages, local health test,
  Docker build/new-image health test, existing service HTTP health. They do not
  establish current container freshness or report correctness.
- T03 attempt 1 is Canceled; attempt 2 is Done by "đẩy lên và chốt t03". Eleven
  offline capture tests passed before the one 11-GET run, all 200, on 2026-11-02
  at 09:33:25-09:33:27 UTC. Its request budget is consumed; do not rerun.
- Private capture: `.local/inspect/T03/20261102T093325641343Z/`, eleven raw bodies
  totaling 76276 bytes, eleven metadata rows, 32 sanitized output rows. Eleven
  readable copies in pretty/ preserve values/order and unchanged raw hashes.
  All remain local/ignored; publish neither payloads nor raw cursors.
- T03 evidence: overlapping request pages and inconsistent totals; two unfinished
  feed pages contain ten rows/eight unique seq values and four request payload IDs.
  Payload updated_at can follow change at. The incomplete capture cannot prove
  historical coverage; insufficient history is candidate-reported. Full acquisition,
  rate limits, expiry, staff refresh, and graded-range correctness remain unverified.
- Revised checks passed: exact six-file scope, 27 local link targets, diff
  whitespace, preserved DECISIONS headings/assumption, review statuses, both stashes,
  ignored/untracked inspection data, and generic credential/known-cursor scan.
  At the pre-review checkpoint HEAD was 7667ed2, the index empty, and PR #7
  rechecked CLOSED. No delivery occurred before acceptance. Manual
  seven-rule/contract and workflow traces passed.
  The 45-minute synthetic example is not execution evidence. No runtime tests
  or live API calls were made; no completeness/readiness/performance claim follows.

## Next action

T04's accepted revision and approved Git delivery are complete. PR #9 merge remains
separately authorized. T03A stays deferred, and T05 needs its own
proposal. Actual total time against the three-hour budget has not been measured.
