---
name: write-decisions
description: Maintain this SLA take-home project's DECISIONS.md during implementation and before submission, recording supported assumptions, API discoveries, AI usage, trade-offs, and remaining work in English.
---

# Write decisions

Keep the root `DECISIONS.md` useful to a reviewer who has not seen the conversation. Record why the implementation behaves as it does and what remains uncertain. This is a short engineering decision record, not a transcript or a replacement for the setup guide.

## Context and evidence

The project root is the directory containing `DECISIONS.md`, `docs/`, and `docker-compose.yml`; for this skill's repository location, it is two directories above the skill folder.

- Read the current `DECISIONS.md` before editing. Preserve the candidate's writing and the four supplied headings.
- Use the current task, inspected code/diff, actual tool results, and the user's reports to identify what changed. Read relevant parts of `docs/rules.md`, `docs/contract.md`, and `docs/api.md` when a decision depends on them. Consult `Requirements.md` only as needed for the brief; it contains credentials.
- Distinguish a documented requirement, a chosen approach, an unverified hypothesis, and an observed result. Attribute a user-reported result when it has not been independently checked.
- Earlier setup notes are historical evidence, not proof of the current environment. Resolve stale claims when new evidence is available. If evidence is missing, omit the claim or state the specific uncertainty; do not run the practice API just to fill this document. Its data begins changing five minutes after the first call.

## When to update

Update after a meaningful implementation checkpoint: an architectural choice, a confirmed API/data surprise, a change in approach, consequential validation, a known limitation, or substantive AI assistance. Prefer a small edit at that checkpoint over reconstructing the work at the end.

If there is nothing new worth recording, leave the file unchanged. Routine edits, every command, and every commit do not need entries. A documentation update does not authorize implementation changes, new API requests, commits, or submission.

## Put information in the right section

Every entry must be supported and match the meaning of its section. A true statement does not automatically belong in DECISIONS.md. Split mixed-purpose sentences and place each part where it belongs.

Keep work progress, pending checks, and environment status in `docs/STATE.md`; keep setup commands and environment troubleshooting details in `docs/development.md`. For example, "No practice API calls have been made during environment setup" is work status, not an API finding. Leave a section empty when no qualifying content exists; do not fill it with an absence-of-work statement.

### What I assumed

Record only assumptions made to resolve genuine gaps in the assignment: what the specification leaves open, the interpretation adopted, and its effect on behavior. Clearly mark interpretations still awaiting a decision. Explicit requirements and technical selections such as a framework or database are not assumptions by themselves. Record a technical choice under trade-offs when its rationale and cost are supported; otherwise keep the descriptive implementation fact in architecture or state documentation.

### What I found in the API or data

Record only actual observations from API responses or inspected data. Identify the evidence with a sanitized endpoint, field, dataset, or reproducible result. Clearly attribute user-reported observations when not independently checked. Explain the consequence and handling when relevant; compare documented and observed behavior when they differ. Include a small non-sensitive example only when useful.

Exclude work status, missing API calls, quoted documentation, and unverified hypotheses from this section. A synthetic test fixture is not evidence of upstream behavior. Put an unresolved investigation in STATE, or a genuine specification-gap assumption under assumptions. Do not infer that all responses behave the same from a single example. When evidence changes an earlier finding, revise it and preserve the relevant reason for the changed approach.

### How I used AI

Describe the tool and concrete assistance actually used: interpreting the brief, planning, code generation, tests, debugging, review, or documentation. Explain how the output was used, material corrections, and related verification actually performed. Record documentation assistance when relevant, including use of this skill. Keep standalone progress and environment status in STATE rather than appending them to an AI-use entry.

Do not claim the candidate wrote, reviewed, understood, or tested generated code unless supported. Do not invent AI mistakes to make the narrative look reflective. Use first person for the candidate only for actions attributable to the candidate; name Codex or another tool for agent actions.

### Trade-offs and what I would do next

Explain a consequential choice as **choice + reason + cost/limitation**. Mention an alternative only if it was actually considered or clearly label it as a future option. Connect trade-offs to the three-hour budget and the ordered report, speed, freshness, and browsing levels where relevant.

State meaningful unfinished delivery work and the next useful step candidly. Keep routine progress in STATE. Update resolved limitations so they no longer read as current blockers. Keep machine-specific installation history in `docs/development.md`; include it here only when it affected delivery or a design choice.

## Writing and validation

- Write concise English bullets under the existing headings. Match the file's level of detail; use plain language the candidate can explain in an interview.
- Prefer one or two sentences per decision. Add the supporting file, test, or sanitized command when it makes the claim assessable; avoid large logs and copied requirements.
- Merge duplicate bullets and revise superseded claims. Preserve useful rationale when an approach changes. Leave a section empty when there is no supported entry.
- Report tests as passed, failed, or not run based on actual evidence. A syntax check is not a runtime test; a health check is not SLA correctness. Performance claims need the measured date range, timing, and relevant conditions; freshness and pagination guarantees need their own evidence. Avoid claiming a whole grading level from one narrow check.
- Never include tokens, authorization headers, `.env` contents, credentials embedded in URLs, or raw cursors. Refer to environment variable names instead.
- Before keeping an entry, verify both its factual support and its semantic fit with the section. Leave sections empty when no qualifying content exists; do not add progress statements to fill them.
- Check the resulting diff against the source facts and section definitions. Ensure the four headings remain, no secrets were copied, speculative work is not presented as complete, and additions explain decisions rather than list files changed. Correct existing misplaced entries within the approved scope instead of preserving them as exceptions.

When reporting back, briefly state which sections changed and any material unresolved point. If no edit was warranted, say so without manufacturing content.
