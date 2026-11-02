# DECISIONS

Write in English. Short bullet points are fine. Reviewers read this file alongside your code.

## What I assumed

<!-- Anything the brief did not say that you had to decide. -->

## What I found in the API or data

<!-- Anything that did not match the docs, or surprised you, and how you handled it. -->

## How I used AI

<!-- Which tools, what you asked, what came back wrong, what you changed. "I didn't use AI" is fine too. -->

- Used Codex to read the brief and starter documentation, configure the development environment, and document verification results.
- Used Codex to create a local `write-decisions` skill and repository context instructions. `docs/STATE.md` separates inspected implementation from historical test results so a later session can resume without treating unverified work as complete.
- Agreed with Codex on a candidate-controlled workflow: each small task and its technical decisions require approval before implementation, followed by a code walkthrough and candidate review. `docs/PLAN.md` records scope and approval separately from implementation and verification so generated code remains reviewable.

## Trade-offs and what I would do next

<!-- What you left out to stay within 3 hours, and what you would do with more time. -->
