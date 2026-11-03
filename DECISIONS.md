# DECISIONS

Write in English. Short bullet points are fine. Reviewers read this file alongside your code.

## What I assumed

<!-- Anything the brief did not say that you had to decide. -->
- I assume the Reviewers are both human and agents
- I assume reverting a reversal does not restore an earlier event. If B reverts A and C reverts B, all three are excluded under rule 2.
- For equal event timestamps, I use event ID as the tie-breaker: the lowest ID is earliest and the highest is latest. The brief does not specify a tie-breaker.
- An overnight work window belongs to its opening weekday; each local calendar day's holiday excludes that portion of the window. Overlapping work windows are unioned rather than counted twice.
- I assume the current request's due_on stays synchronized with the site-local date of the latest eligible event due_at. This is not independently verified; due_on has no time component, so rule 6 still uses the event due_at, including its time, rather than replacing it with due_on. Historical event deadlines need not all match the current request date.

## What I found in the API or data

<!-- Anything that did not match the docs, or surprised you, and how you handled it. -->

- The replacement T03 sample on 2026-11-02 returned 100 distinct IDs on each of two request pages; page 1's last request reappeared first on page 2 with the same payload. Both reported `total=11999`, `per_page=100`, and `total_pages=122`, while `ceil(total/per_page)=120`. The cause and full-traversal completeness remain unresolved; removing duplicates alone would not establish that no requests were missed.
- Offline review of the two saved change-feed pages found ten rows but only eight distinct `seq` values: page 1's last two rows reappeared first on page 2 with identical payloads. All five request-payload occurrences had `updated_at` later than the change's `at`, supporting the documented current-payload behavior rather than event-time snapshots. The sample does not establish general freshness, cursor expiry, or staff-change handling.
- The request sample covers 30 October through 2 November in UTC, not the graded 12-18 October range. The selected request had one pending event with a null actor, so first response, reversals, completion/reopening, meaningful event ordering, and event pagination remain unexercised; only two of three sites' holiday lists were sampled.
- The candidate reports that the feed does not contain the full history. Offline review of the retained T03 bodies found two unfinished change pages (ten rows, eight distinct seq values, four request payload IDs, both has_more=true). This sample cannot independently establish the feed's historical coverage or retention window.
- The candidate reports that the 12 October 2026 report contains rows showing only ID and site, with the remaining displayed fields blank/null. The corresponding response bodies and event histories have not been independently checked, so the cause remains unverified.

## How I used AI

<!-- Which tools, what you asked, what came back wrong, what you changed. "I didn't use AI" is fine too. -->

- Used Codex to analyze the brief, SLA rules, API documentation and grading contract, and to break the work into tasks ordered by the assignment's levels.

- Discussed and agreed on a candidate-controlled workflow with Codex: scope and technical decisions require my approval before implementation, followed by explanations and review. I later requested grouping the remaining level-one work into a runnable MVP.

- Used Codex to draft and maintain DECISIONS.md, architecture notes, task records and session handoffs. Codex also helped create a local write-decisions skill to distinguish requirements, assumptions, observations and unverified claims.

- Used Codex to explore implementation choices and their costs. Codex initially proposed bootstrapping from the change feed alone; after I pointed out that it lacked complete history, the design changed to loading baseline requests and full event histories.

- Used Codex to implement the SLA calculations, data acquisition, in-memory storage, report endpoint and page, and to generate synthetic and mock tests. Codex ran checks locally and in Docker; the recorded suite passed 53 tests. These checks do not independently establish correctness on the live dataset.

- Used Codex to build private API-response capture and analyze retained evidence, including repeated pagination rows and request changes between acquisition walks. I performed manual report checks and reported unexpected results; Codex helped document them without treating unverified explanations as confirmed causes.

## Trade-offs and what I would do next

<!-- What you left out to stay within 3 hours, and what you would do with more time. -->

- I used plain HTML, CSS and JavaScript to minimize setup and build tooling within the time budget. The UI is a basic report table, with DOM updates, loading and error handling managed manually.
- A bounded sample with private raw capture permits detailed offline investigation without spending further API calls. It does not prove full coverage, and raw files are unavailable to public-repository reviewers; the task record provides sanitized evidence while the source bodies remain on the local machine.
- M01 loads baseline data from request pages and full per-request event histories rather than relying on incomplete feed history. This has a higher HTTP cost; initial conflict/retry/reconciliation policies are implemented, but acquisition completeness is unproven and feed updates remain deferred.
- I used one worker with process-local memory instead of a database to avoid schema, migration and persistence setup within the time budget. Restarting requires a full reload, workers cannot share the store, and copied snapshots increase memory usage. Successful real-data report validation remains incomplete.

- M01 uses three full request walks and sequential bounded HTTP to detect observed inconsistencies before publication, at substantial first-load cost. Sequential requests simplify rate and retry control but increase initial loading time; performance targets remain unverified. Stable walks cannot prove that the upstream omitted nothing, and no automatic refresh is provided; snapshots remain cached for subranges until another load or restart. Running the report again for a cached range reuses that snapshot rather than fetching fresh upstream data, so the report may be stale.
- Ambiguous/nonexistent local wall times fail rather than silently selecting a DST offset. With more time, I would clarify the intended business interpretation and extend timezone/DST fixtures before supporting those cases.

With more time, I would prioritize the following work in the assignment's level order:

1. Complete the level 1 evidence first: restore a reliable upstream connection, approve a new bounded verification run, and demonstrate October and 12-18 October reports with source-to-row walkthroughs and manual UI feedback. The failed live load and 53 passing offline tests do not establish end-to-end correctness.
2. Investigate pagination completeness and baseline consistency using retained evidence and controlled change tests. Three agreeing request walks are only a practical check; I would seek an upstream snapshot or stable pagination boundary if available rather than claim that matching counts prove coverage.
3. Extend and measure six-month acquisition/readiness/report performance. I would measure request cost before choosing bounded concurrency, avoid flooding rate limits, and evaluate durable storage such as SQLite plus resumable loading to reduce restart cost. Those are future options, not current guarantees.
4. Add idempotent change-feed updates, current staff refresh, and cursor-expiry/recovery checks, measuring visibility against the 60-second target. The feed would update a complete baseline rather than replace its missing history.
5. Implement browse filters/sorts and a cursor strategy tested under concurrent changes for exactly-once appearance. I would also add operational metrics for load progress, retry counts and snapshot age, while keeping private raw evidence out of public logs.
