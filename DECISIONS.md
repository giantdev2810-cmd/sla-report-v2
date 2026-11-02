# DECISIONS

Write in English. Short bullet points are fine. Reviewers read this file alongside your code.

## What I assumed

<!-- Anything the brief did not say that you had to decide. -->
- I assume the Reviewers are both human and agents
- I assume reverting a reversal does not restore an earlier event. If B reverts A and C reverts B, all three are excluded under rule 2.

## What I found in the API or data

<!-- Anything that did not match the docs, or surprised you, and how you handled it. -->

- The replacement T03 sample on 2026-11-02 returned 100 distinct IDs on each of two request pages; page 1's last request reappeared first on page 2 with the same payload. Both reported `total=11999`, `per_page=100`, and `total_pages=122`, while `ceil(total/per_page)=120`. The cause and full-traversal completeness remain unresolved; removing duplicates alone would not establish that no requests were missed.
- Offline review of the two saved change-feed pages found ten rows but only eight distinct `seq` values: page 1's last two rows reappeared first on page 2 with identical payloads. All five request-payload occurrences had `updated_at` later than the change's `at`, supporting the documented current-payload behavior rather than event-time snapshots. The sample does not establish general freshness, cursor expiry, or staff-change handling.
- The request sample covers 30 October through 2 November in UTC, not the graded 12-18 October range. The selected request had one pending event with a null actor, so first response, reversals, completion/reopening, meaningful event ordering, and event pagination remain unexercised; only two of three sites' holiday lists were sampled.
- The candidate reports that the feed does not contain the full history. Offline review of the retained T03 bodies found two unfinished change pages (ten rows, eight distinct seq values, four request payload IDs, both has_more=true). This sample cannot independently establish the feed's historical coverage or retention window.

## How I used AI

<!-- Which tools, what you asked, what came back wrong, what you changed. "I didn't use AI" is fine too. -->

- Used Codex to read the brief and starter documentation, configure the development environment, and document verification results.
- Used Codex to create a local `write-decisions` skill and repository context instructions. `docs/STATE.md` separates inspected implementation from historical test results so a later session can resume without treating unverified work as complete.
- Agreed with Codex on a candidate-controlled workflow: each small task and its technical decisions require approval before implementation, followed by a code walkthrough and candidate review. `docs/plan/PLAN.md` records scope and approval separately from implementation and verification so generated code remains reviewable.
- Codex adapted the canceled inspection script to retain local raw bodies and generated offline tests for byte preservation, request limits, safe output, and failure handling. Eleven tests passed before the replacement live run; Codex reconciled eleven saved bodies with metadata/output, then identified repeated feed sequences and post-change payload timestamps through offline review. The local `write-decisions` skill guided these evidence-based notes; capture checks do not establish SLA correctness.
- Codex initially proposed feed-only bootstrap without established historical coverage. After the candidate confirmed that history is incomplete, Codex revised the approved T04 design to request/event baseline loading and feed updates, leaving other questions explicitly open. The local `write-decisions` skill guided separating candidate-reported facts, bounded capture evidence, and design choices. The candidate also requested PR creation only after review and acceptance; this architecture is not an implemented or tested report.
- Codex implemented the pure rule-2 filter and synthetic tests after candidate approval, including the agreed non-restoring reversal chain. Ten rule cases and the existing health test passed; these checks cover the helper's behavior, not live data completeness or the remaining SLA rules. The local `write-decisions` skill guided recording the interpretation as an assumption rather than an API finding.

## Trade-offs and what I would do next

<!-- What you left out to stay within 3 hours, and what you would do with more time. -->

- A bounded sample with private raw capture permits detailed offline investigation without spending further API calls. It does not prove full coverage, and raw files are unavailable to public-repository reviewers; the task record provides sanitized evidence while the source bodies remain on the local machine.
- The approved revision replaces feed-only bootstrap with request pages plus full per-request event histories, using the feed for updates. This avoids depending on the feed for initial history at greater HTTP cost; acquisition completeness, bootstrap/feed coordination, rate limits, and conflict policies remain open rather than implemented guarantees.
- The initial design selects one worker with process-local memory rather than SQLite to limit database work within the time budget. Restart requires a full reload, multiple workers would have separate stores, and consistent read snapshots add memory/copying cost. Pure SLA calculations separate rule verification from network and storage behavior; these modules are not implemented yet.
