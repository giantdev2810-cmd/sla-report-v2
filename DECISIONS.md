# DECISIONS

Write in English. Short bullet points are fine. Reviewers read this file alongside your code.

## What I assumed

<!-- Anything the brief did not say that you had to decide. -->
- I assume the Reviewers are both human and agents

## What I found in the API or data

<!-- Anything that did not match the docs, or surprised you, and how you handled it. -->

- The replacement T03 sample on 2026-11-02 returned 100 distinct IDs on each of two request pages, with one ID shared between pages and identical payloads for that ID. Both responses reported `total=11999`, `per_page=100`, and `total_pages=122`, while `ceil(total/per_page)=120`. The capture preserves this discrepancy for offline review; its cause and full-traversal behavior remain unresolved before ingestion design in T04.
- The selected request had only one event (a null actor and a local deadline string), so it did not establish reversal handling, meaningful event ordering, or event pagination. Two five-row change-feed pages accepted cursor continuation with ascending sequences within each page; expiry, duplicate delivery, and current-payload semantics remain unverified.

## How I used AI

<!-- Which tools, what you asked, what came back wrong, what you changed. "I didn't use AI" is fine too. -->

- Used Codex to read the brief and starter documentation, configure the development environment, and document verification results.
- Used Codex to create a local `write-decisions` skill and repository context instructions. `docs/STATE.md` separates inspected implementation from historical test results so a later session can resume without treating unverified work as complete.
- Agreed with Codex on a candidate-controlled workflow: each small task and its technical decisions require approval before implementation, followed by a code walkthrough and candidate review. `docs/plan/PLAN.md` records scope and approval separately from implementation and verification so generated code remains reviewable.
- Codex adapted the canceled inspection script to retain local raw bodies and generated offline tests for byte preservation, request limits, safe output, and failure handling. Eleven tests passed before the replacement live run; Codex then reconciled eleven saved bodies with metadata/output and used the local `write-decisions` skill to document the supported findings. These checks do not establish SLA correctness.

## Trade-offs and what I would do next

<!-- What you left out to stay within 3 hours, and what you would do with more time. -->

- A bounded sample with private raw capture permits detailed offline investigation without spending further API calls. It does not prove full coverage, and raw files are unavailable to public-repository reviewers; the task record provides sanitized evidence while the source bodies remain on the local machine.
