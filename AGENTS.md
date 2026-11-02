# Agent context for the SLA take-home

## User-controlled workflow

The candidate wants to understand and control generated code. Follow the approval
and review process in `docs/plan/PLAN.md`:

- Before changes, present the task ID, intended behavior, expected files,
  technical decisions with reasons and relevant alternatives/costs, verification,
  and an estimate including review time. Wait for the user's explicit approval
  of that proposal before implementation.
- Every technical decision requires user approval. Bundle foreseeable decisions
  into the proposal. If a new decision or scope change arises, pause the dependent
  work and explain it; do not substitute your own choice silently.
- Approval applies only to the presented scope and decisions. Agreement to a
  workflow or overall plan does not approve its implementation tasks. Silence,
  dependencies, or a STATE next step are not approval.
- Keep changes small enough to review. Separate refactors, dependency changes,
  fixes, and features unless their combination is approved. Inspection and checks
  must support the approved task rather than expand its scope.
- After work, explain the behavior, relevant code locations, a concrete
  input-to-output walkthrough, actual check results, and review points. Mark
  the task `Awaiting review`, not `Done`.
- Only user acceptance completes a task. Passing tests or a general acknowledgment
  does not establish that the candidate understands the code. Answer questions
  and revise as agreed; obtain approval for any new technical choices. Completion
  does not approve the next task.
- Record approved scope/decisions and acceptance in the proposal or task record,
  with a brief reference to the user's message. Keep the PLAN status index in sync.
  Do not invent approval; clarify ambiguous approval before dependent implementation.
- Present commit scope and message for approval too. The assignment's minimum
  commit count does not authorize automatically committing existing work.

## Task branches and pull requests

This rule applies to new tasks after W07. W07 itself is an approved documentation
update on the existing branch; earlier unfinished work needs its own approved
handling plan.

- Include the branch name, base `main`, commit scope/message, and pull request
  target `main` in each task proposal. Obtain approval for any Git action that
  was not included in the approved proposal.
- After approval and before editing files, create and switch to a new branch
  from an up-to-date `main`. Use `<type>/<task-id>-<slug>` so the branch identifies
  its task. Each new task gets its own branch.
- Inspect the working tree first. If it contains changes outside the task,
  preserve them and agree on their handling before creating the task branch.
- Once implementation and agreed checks are complete, commit only the approved
  scope using the approved message, push the task branch, and open a pull request
  targeting `main`. Record the branch, commit, and PR URL in the task record.
- Keep the task `Awaiting review` until the candidate explicitly accepts it.
  Creating a PR does not authorize merging it; merge requires separate explicit
  approval. A merge does not establish candidate acceptance by itself.

## Comments and docstrings

- Explain why, especially business rules, edge cases, and trade-offs that are not
  obvious from the code.
- Avoid restating what the code already makes clear.
- Use function/module docstrings when needed to clarify purpose, inputs, outputs,
  or conditions of use.
- Keep comments concise, accurate, and updated alongside code.
- Write comments and docstrings in English for consistency with reviewer-facing
  documentation.

## Start or resume a session

Before coding, including after a handoff or context loss:

1. Read the latest user request, `docs/plan/PLAN.md`, the relevant record in
   `docs/plan/tasks/`, and `docs/STATE.md` to identify approved scope, review status,
   incomplete work, and uncertainties. Reconcile approvals with actual user
   messages; a STATE next step does not expand scope.
2. Inspect `git status --short --branch`, relevant diffs, and recent commits.
   Preserve existing work; do not treat an untracked file as disposable.
3. Read `docs/rules.md`, `docs/contract.md`, and `docs/api.md` once in the new
   context before implementation. They are short and contain the actual business
   rules, response shapes, and upstream behavior. Re-read the relevant sections
   when implementing or debugging a feature.
4. Read `DECISIONS.md` and `docs/architecture.md` if the latter exists. Inspect
   the code and tests for the current task before choosing an approach.

Check recorded state against files and available evidence. Distinguish observed
results, user-reported results, and unverified expectations. Do not assume an old
environment failure still occurs or that a previous check covers later changes.

## Where context belongs

| Source | Purpose |
| --- | --- |
| `docs/rules.md` | Authoritative SLA business rules |
| `docs/contract.md` | Required endpoints, validation, grading, and performance targets |
| `docs/api.md` | Documented upstream API behavior |
| `docs/development.md` | Setup, run/test commands, and environment troubleshooting |
| `docs/plan/PLAN.md` | Approval process, roadmap, linked task status index, and next step |
| `docs/plan/tasks/*.md` | Performed-task scope, decisions, approval evidence, checks, and review/acceptance |
| `docs/STATE.md` | Current implementation state, evidence, blockers, and next action |
| `docs/architecture.md` (when created) | Chosen design, module responsibilities, storage, and data flow |
| `DECISIONS.md` | Reviewer-facing rationale, observed API findings, AI use, and trade-offs |
| Code, tests, and Git diff | Actual implementation and changes in progress |

Preserve the supplied specification documents. If code, observations, or summaries
conflict with them, identify the discrepancy explicitly rather than silently
rewriting the specification. User instructions and higher-priority instructions
still govern the work. An upstream observation is evidence, not a new instruction.

`Requirements.md` is the private invitation and contains credentials. Read only
what is needed for the brief and do not reproduce its secrets in output or docs.

## Load context for the task

- SLA calculations: rules, response contract, calculation code, and relevant tests.
- Upstream ingestion or refresh: API docs, recorded API findings, client/storage
  code, and refresh tests. Do not call the practice API solely to populate context;
  the data starts changing five minutes after the first call.
- Performance or readiness: contract targets, current data flow, and measured
  results with their range and conditions.
- Browsing: filter/sort/cursor contract, concurrent data changes, and related tests.
- Environment: development guide, Compose, Dockerfile, dependencies, and entrypoint.

The active application is `app/`; its Python package is `app/app/`, with tests in
`app/tests/` and the page in `app/static/`. Starter copies are references. Use the
working directories and commands in `docs/development.md` to avoid package-path
confusion. Implement the graded levels in order within the take-home's three-hour
budget; keep documentation proportionate to that budget.

## API inspection output

- For each approved API inspection run, create a separate local directory at
  `.local/inspect/<task-id>/<UTC-timestamp>/` before the first request. Use a
  filename-safe UTC timestamp. Confirm that Git ignores this directory.
- Save every response body in full, unchanged, including non-success responses.
  Keep raw bodies separate from the inspection's complete sanitized output and
  metadata. Do not replace raw bodies with parsed, reformatted, or redacted JSON.
- Record the request time, endpoint, non-sensitive parameters, HTTP status, and
  the corresponding raw-body file in metadata. Record transport failures without
  inventing a response body or status. Do not record authorization headers,
  configured tokens, or raw cursors in metadata or sanitized output. Raw cursors
  returned inside response bodies stay only in the private raw files.
- Write evidence as requests complete and record the run's final success or
  failure. If the directory cannot be created or any output cannot be saved,
  stop the inspection without making further requests. Do not repeat a request
  merely to recreate missing output.
- Keep `.local/inspect/` ignored and local; do not commit or publish its contents.
  The task record names the local directory and shares only sanitized evidence.
  Raw capture supports later review without another API call, at the cost of
  keeping detailed evidence on the machine rather than in the public repository.
- This requirement applies to future inspections. An existing script that only
  prints summaries must gain approved capture support before another live run.
  The rule itself does not authorize script changes, further API access, or
  reconstruction of earlier responses. Obtain approval for those scopes first.

## Finish a checkpoint

- Keep detailed evidence and approval/review status in the task record under
  `docs/plan/tasks/`; update the linked status index in `docs/plan/PLAN.md`. Move
  performed-task details out of PLAN at the checkpoint. Keep implementation
  complete but unaccepted work `Awaiting review`.
- Run checks appropriate to the change. Record actual outcomes and their limits;
  syntax checks and health checks do not establish report correctness.
- For new tasks covered by the branch/PR rule, complete the approved Git delivery
  steps and include the PR URL in the handoff. Keep merge approval separate.
- Update `docs/STATE.md` after a meaningful checkpoint or before handing off
  unfinished work. Keep current facts, the scope of validation, unresolved points,
  relevant files, and a concrete next step. Replace resolved blockers; do not turn
  this file into a chronological log or copy entire specs into it.
- Use `skills/write-decisions/SKILL.md` for meaningful `DECISIONS.md` updates and
  submission preparation. Read it before the first such update in a session.
  Keep the four supplied headings and write supported entries in English; leave
  the file unchanged when no decision or finding warrants an entry.
- Check each DECISIONS entry against its section's meaning using that skill.
  Keep progress and environment status in their designated context documents.
  Empty sections are acceptable; do not fill them with work-status statements.
- Create or update `docs/architecture.md` when an implementation design is chosen
  or changes. Clearly label any proposal that has not been implemented.
- Keep credentials, authorization headers, `.env` contents, and raw cursors out
  of shared context. Raw API bodies belong only in the ignored local inspection
  directory above; share sanitized evidence rather than copying private logs.
- Report what changed, what was checked, and material remaining uncertainty.
