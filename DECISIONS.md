# DECISIONS

Write in English. Short bullet points are fine. Reviewers read this file alongside your code.

## What I assumed

<!-- Anything the brief did not say that you had to decide. -->
- I assume the Reviewers are both human and agents

## What I found in the API or data

<!-- Anything that did not match the docs, or surprised you, and how you handled it. -->

- The replacement T03 sample on 2026-11-02 returned 100 distinct IDs on each of two request pages; page 1's last request reappeared first on page 2 with the same payload. Both reported `total=11999`, `per_page=100`, and `total_pages=122`, while `ceil(total/per_page)=120`. The cause and full-traversal completeness remain unresolved; removing duplicates alone would not establish that no requests were missed.
- Offline review of the two saved change-feed pages found ten rows but only eight distinct `seq` values: page 1's last two rows reappeared first on page 2 with identical payloads. All five request-payload occurrences had `updated_at` later than the change's `at`, supporting the documented current-payload behavior rather than event-time snapshots. The sample does not establish general freshness, cursor expiry, or staff-change handling.
- The request sample covers 30 October through 2 November in UTC, not the graded 12-18 October range. The selected request had one pending event with a null actor, so first response, reversals, completion/reopening, meaningful event ordering, and event pagination remain unexercised; only two of three sites' holiday lists were sampled.

## How I used AI

<!-- Which tools, what you asked, what came back wrong, what you changed. "I didn't use AI" is fine too. -->

- Used Codex to read the brief and starter documentation, configure the development environment, and document verification results.
- Used Codex to create a local `write-decisions` skill and repository context instructions. `docs/STATE.md` separates inspected implementation from historical test results so a later session can resume without treating unverified work as complete.
- Agreed with Codex on a candidate-controlled workflow: each small task and its technical decisions require approval before implementation, followed by a code walkthrough and candidate review. `docs/plan/PLAN.md` records scope and approval separately from implementation and verification so generated code remains reviewable.
- Codex adapted the canceled inspection script to retain local raw bodies and generated offline tests for byte preservation, request limits, safe output, and failure handling. Eleven tests passed before the replacement live run; Codex reconciled eleven saved bodies with metadata/output, then identified repeated feed sequences and post-change payload timestamps through offline review. The local `write-decisions` skill guided these evidence-based notes; capture checks do not establish SLA correctness.
- Codex documented the approved T04 data flow, module boundaries, and a synthetic rule walkthrough, using the local `write-decisions` skill to distinguish design choices from API evidence. The resulting architecture is not an implemented or tested report.

## Trade-offs and what I would do next

<!-- What you left out to stay within 3 hours, and what you would do with more time. -->

- A bounded sample with private raw capture permits detailed offline investigation without spending further API calls. It does not prove full coverage, and raw files are unavailable to public-repository reviewers; the task record provides sanitized evidence while the source bodies remain on the local machine.
- The approved initial design uses the change feed for request/event bootstrap instead of request pages plus per-request event calls, avoiding reliance on the sampled request pagination discrepancy. Complete historical feed coverage still needs verification during integration; it cannot be inferred from T03's two-page sample.
- The initial design selects one worker with process-local memory rather than SQLite to limit database work within the time budget. Restart requires a full reload, multiple workers would have separate stores, and consistent read snapshots add memory/copying cost. Pure SLA calculations separate rule verification from network and storage behavior; these modules are not implemented yet.
