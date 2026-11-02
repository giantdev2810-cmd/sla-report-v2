# DECISIONS

Write in English. Short bullet points are fine. Reviewers read this file alongside your code.

## What I assumed

<!-- Anything the brief did not say that you had to decide. -->
- I assume the Reviewers are both human and agents

## What I found in the API or data

<!-- Anything that did not match the docs, or surprised you, and how you handled it. -->

- A bounded sample on 2026-11-02 found one shared request ID between pages 1 and 2 (`per_page=100`). Both pages reported `total=11986` and `total_pages=122`, which differs from `ceil(total/per_page)=120`. These observations do not establish the cause or a complete acquisition strategy; T04 must account for the uncertainty before ingestion is implemented.
- The sampled request had only one event, with a null actor and a site-local deadline string. It does not establish event pagination, reversal handling, or multi-event ordering; two sampled change-feed pages accepted cursor continuation but do not establish expiry or duplicate behavior.

## How I used AI

<!-- Which tools, what you asked, what came back wrong, what you changed. "I didn't use AI" is fine too. -->

- Used Codex to read the brief and starter documentation, configure the development environment, and document verification results.
- Used Codex to create a local `write-decisions` skill and repository context instructions. `docs/STATE.md` separates inspected implementation from historical test results so a later session can resume without treating unverified work as complete.
- Agreed with Codex on a candidate-controlled workflow: each small task and its technical decisions require approval before implementation, followed by a code walkthrough and candidate review. `docs/plan/PLAN.md` records scope and approval separately from implementation and verification so generated code remains reviewable.
- Codex generated a bounded inspection script and used the local `write-decisions` skill to document the resulting observations. Offline mocks checked the request ceiling, redacted output, cursor forwarding, and stopping on 429 before an 11-GET live sample; these checks do not verify the SLA report.

## Trade-offs and what I would do next

<!-- What you left out to stay within 3 hours, and what you would do with more time. -->
