# Work plan and review process

## Agreement and current authorization

The candidate requested small reviewable tasks, explanations before actions,
approval of every technical decision with its rationale, and short reports after
implementation. The candidate agreed to the proposed workflow in the message
"ừ" immediately after that discussion. This authorizes documenting the workflow
and drafting this plan, not implementing the roadmap below.

Task **W01 — document the workflow**: update `../AGENTS.md`, create this
plan, and update `STATE.md` and the AI documentation in `../DECISIONS.md`.
Verification covers document consistency, references, and whitespace.
Status: **Awaiting review**. User acceptance is pending. No application code, API
discovery, dependency installation, or new commit is included in W01.

Task **W02 — correct DECISIONS section semantics**:

- Scope: update `../skills/write-decisions/SKILL.md` and related AGENTS guidance;
  remove the misplaced API-call status and framework selection from DECISIONS.
  Keep pure environment status in STATE, including the status previously appended
  to an AI-use sentence. Do not invent a rationale to populate trade-offs.
- Approval: the user's message "duyệt cả 2", following the proposal covering both
  rule changes and DECISIONS corrections, approves these changes.
- Decisions: enforce each heading's meaning; assumptions resolve specification
  gaps, API findings require observations, and empty sections are acceptable.
  AGENTS points to the skill rather than duplicating its definitions.
- Verification: skill-creator validator, document consistency, and whitespace.
- Result: skill and AGENTS now require factual support and correct section
  placement. Removed the API-call status and framework selection from DECISIONS;
  removed standalone environment status from its AI-use entry. The implementation
  facts remain in STATE. No unsupported trade-off rationale was added.
- Checks: skill-creator validator returned `Skill is valid!`; document inspection,
  whitespace checks, and `git diff --check` passed. Structural validation does not
  prove future writing behavior. No runtime test was needed for these docs.
- Status: **Awaiting review**; user acceptance of the result is pending.
- Bookkeeping: update this record and STATE without changing application code,
  dependencies, practice API data, or Git history.

Current task **W03 — publish the existing work on a GitHub branch**:

- Approval: the user requested pushing all work on a branch, then selected
  "Tạo repository mới public tên sla-report-v2" when asked for the destination.
- Destination: new public repository `giantdev2810-cmd/sla-report-v2`, using the
  account confirmed by the GitHub connection. Local branch/message presented:
  `chore/setup-agent-context` and
  `chore: prepare FastAPI workspace and agent context`.
- Scope: retain the original starter commit and publish the current setup,
  documentation, skill, and application starter. Exclude credentials and local
  generated files. Publishing does not imply acceptance of W01/W02 or approval
  to implement the roadmap.
- Checks: scanned 74 tracked/unignored candidate files for the actual practice
  token and private/generated paths; no matches found. Git confirmed `.env`,
  `Requirements.md`, `.venv`, and `.uv-cache` are ignored. Whitespace check passed.
- Status: **Blocked**. The session cannot write `.git`; creating the branch failed
  while locking its ref. No branch or commit was created. No remote is configured.
  The CLI cannot reach GitHub through the session's configured proxy. Its auth
  error alone therefore does not establish whether the saved token is invalid.
  The connected plugin identifies the account but has no repository-creation tool.
- Next action: run the prepared Git/GitHub commands from an ordinary user terminal,
  or resume in a session with Git metadata write access and working GitHub access.
  Repository creation and push have not been confirmed.

## Approval and review loop

1. Prepare a small task proposal using context inspection within authorized scope.
2. Present it in Vietnamese using the fields below. Keep maintained docs in English.
3. Wait for approval of the specific task scope and technical decisions.
4. Implement that scope and run agreed checks. Pause dependent work if new
   decisions arise; present their rationale before making them.
5. Explain what changed, code locations, one input-to-output walkthrough, actual
   check results/limitations, and points needing candidate review.
6. Mark `Awaiting review`. Answer questions and revise as agreed. Mark `Done`
   only when the candidate accepts; obtain approval for the next task.

The goal is behavior the candidate can explain in an interview. Do not claim
understanding on the candidate's behalf or turn review into a memorization test.

## Task proposal and completion record

Create one compact record when a task is proposed. Do not pre-fill speculative
technical decisions for the whole roadmap.

| Field | What to record |
| --- | --- |
| ID and goal | One behavior or tightly related unit of work |
| Dependencies | Prior tasks or unresolved conditions |
| Scope | Expected files, included work, and important boundaries |
| Decisions | Proposed choice, reason, relevant alternative, and cost/limitation; approval tracked separately |
| Acceptance | Observable results the candidate can review |
| Verification | Meaningful examples/checks and their scope |
| Estimate | Implementation plus explanation/review time; revise transparently if needed |
| Approval | User message reference and approved scope/decisions, or pending |
| Result | Actual files, walkthrough, check outcomes, and uncertainty |
| Review | Questions, revisions, and explicit user acceptance, or pending |

Statuses: `Draft` (outline), `Proposed` (concrete scope awaiting approval),
`Approved`, `In progress`, `Awaiting review`, `Done` (user accepted), and `Blocked`
(a named dependency prevents progress). A failed check does not authorize a scope
expansion. Approval of this document is not blanket implementation approval.

## Draft roadmap

All tasks below are **Draft**. Technical decisions and execution approval are
pending. Criteria come from the supplied specification; implementation approaches
remain to be proposed. Explain proposed regrouping and split further if the diff
would be difficult to review.

### Preparation

| ID | Small unit of work | Acceptance / review focus |
| --- | --- | --- |
| T01 | Check environment availability | Current Docker daemon and pinned dependency evidence, distinguished from historical failures |
| T02 | Resolve environment issues if needed | Approve needed changes first; demonstrate starter build, health, and tests with limits stated |
| T03 | Inspect the practice API with an agreed request scope | Sanitized representative data and pagination observations; first-call data-change timer explained before access |
| T04 | Choose initial data flow and module boundaries | User approves responsibilities, data access, storage if any, and costs; record chosen design in architecture.md |

### Level 1: correct report

| ID | Small unit of work | Acceptance / review focus |
| --- | --- | --- |
| T05 | Exclude reversed events | Reverting and referenced events excluded from downstream rules; examples explain chosen interpretation |
| T06 | Determine request inclusion | Inclusive site-local creation dates; canceled, deleted, and merged requests excluded |
| T07 | Calculate business duration | Timezone, hours, holidays, seconds summed before flooring to minutes, and earlier-response zero case |
| T08 | Determine response fields and target result | Earliest eligible processing actor, current staff name, thresholds, and response nulls |
| T09 | Determine completed-late result | Last eligible completion, latest eligible deadline, local parsing, strict comparison, and null cases |
| T10 | Assemble rows and responder summary | Required fields/types; responder counts agree with included rows |
| T11 | Implement report endpoint validation/output | Contract JSON and 400 for missing/invalid/reversed dates; error-handling choices approved first |
| T12 | Show the report on the starter page | Date selection, rows, summary, and understandable loading/error behavior |
| T13 | Review level 1 end to end | Candidate traces a request from source to report; rule checks and representative report results recorded |

T05–T10 can use agreed local examples before live integration. Fixtures, function
interfaces, tests, libraries, and file layout must be proposed for approval. The
order above does not select a particular architecture.

### Levels 2–4, in grading order

| ID | Small unit of work | Acceptance / review focus |
| --- | --- | --- |
| T14 | Acquire and retain six-month report data | Approved ingestion/storage; pagination, bounded API use, and retry behavior |
| T15 | Add readiness and measure performance | Ready means usable data; record month/six-month timings against contract targets and any limitations |
| T16 | Apply upstream changes | Approved refresh/recovery approach; relevant changes visible within 60 seconds, including current staff names |
| T17 | Add browse filters and sorting | Contract filters, sort directions, null placement, and tie order checked |
| T18 | Add cursor pagination | Approved cursor strategy; invalid cursors rejected and continuously matching rows appear exactly once during changes |
| T19 | Add page browsing controls | Candidate can use filters/sorting/paging and explain their endpoint interaction |

These later tasks are outlines. Split T14, T16, and T18 further once observations
and design make their scope concrete. Do not start a later level automatically.

### Delivery

| ID | Small unit of work | Acceptance / review focus |
| --- | --- | --- |
| T20 | Verify delivery claims | Agreed Docker and level-specific checks; separate passed, failed, and unrun evidence |
| T21 | Review decisions, handoff, and demo outline | Accurate English notes; candidate explains design, an SLA example, limitations, and AI use in an approximately three-minute demo |
| T22 | Prepare submission contents | At least five real commits across the work, approved individually; requested archive/repo and video prepared without credentials or unnecessary dependencies |

Commit checkpoints should follow accepted coherent work, not manufacture history
at the end. Preparing artifacts does not authorize public publishing, video upload,
or assessment submission.

## Time budget and next step

The assignment caps work at three hours. Include approvals, explanations, review,
commits, and demo preparation in estimates. Actual time used has not been measured.
Reassess the budget at checkpoints; propose scope reductions and document
unfinished work honestly.

W03 publication is blocked pending normal Git/GitHub access. W01 and W02 remain
awaiting user acceptance. The next suggested implementation proposal remains
T01: inspect current environment
availability and report evidence. Starting Docker, installing dependencies,
changing versions, calling the practice API, and editing application code require
an approved scope and rationale; this roadmap alone does not authorize them.
