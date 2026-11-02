# Work plan and review process

## Document layout

This file contains the approval/review process, roadmap, task status index, and
next step. Detailed records of performed work live in [tasks/](tasks/), including
work Awaiting review. Task records preserve approval evidence and actual results;
only explicit candidate acceptance changes a task to Done.

Read [AGENTS](../../AGENTS.md), this plan, the relevant task record, and
[STATE](../STATE.md) when resuming. STATE holds the current implementation and
validation snapshot; it does not grant permission to start another task.

## Task status index

| Task | Goal | Status |
| --- | --- | --- |
| [W01](tasks/W01.md) | Document the workflow | Awaiting review |
| [W02](tasks/W02.md) | Correct DECISIONS section semantics | Awaiting review |
| [W03](tasks/W03.md) | Publish existing work on a GitHub branch | Awaiting review |
| [W05](tasks/W05.md) | Document comment and docstring principles | Done |
| [W06](tasks/W06.md) | Separate the plan from task records | Done |
| [W07](tasks/W07.md) | Require a separate branch and PR for each new task | Done |
| [W08](tasks/W08.md) | Require local raw API inspection evidence | Done |
| [T01](tasks/T01.md) | Check environment availability | Done |
| [T02](tasks/T02.md) | Install pinned dependencies and verify the starter | Done |
| [T03 attempt 1](tasks/T03-attempt-1.md) | Inspect a bounded practice API sample (canceled first attempt) | Canceled |
| [T03 attempt 2](tasks/T03.md) | Restart inspection with private raw capture | Done |
| [T04](tasks/T04.md) | Choose initial data flow and module boundaries | Done |

## Approval and review loop

1. Prepare a small task proposal using context inspection within authorized scope.
   Include its branch name, base `main`, commit scope/message, and PR target `main`.
2. Present it in Vietnamese using the fields below. Keep maintained docs in English.
3. Wait for approval of the specific task scope and technical decisions.
4. For each new task after W07, inspect the working tree and agree on handling
   any unrelated changes. After approval, create and switch to a new branch from
   up-to-date `main` before editing. Use `<type>/<task-id>-<slug>`. Implement the
   approved scope and run agreed checks. Pause dependent work if new decisions
   arise; present their rationale before making them.
5. After implementation and checks, explain what changed, code locations, one
   input-to-output walkthrough, actual
   check results/limitations, and points needing candidate review.
6. Mark the task record and index `Awaiting review`. Do not create a PR, including
   a draft PR. Answer questions and revise
   as agreed. Mark `Done` only when the candidate accepts; obtain approval for
   the next task.
7. Only after candidate review and explicit acceptance of the completed task,
   open the approved PR targeting `main`. Follow the proposal's approved scope,
   message, and timing for commit/push; earlier approval to commit/push does not
   authorize a PR before review. Record acceptance evidence, actual branch,
   commit, and PR URL. Obtain approval for Git actions missing from the proposal.
8. Merge a PR only with separate explicit approval. Creating a PR or accepting
   a task does not authorize merging; merging alone does not accept the task.

This review gate was requested in the revised T04 proposal and approved by the
user's "duyệt". It applies to T04 and active, future, and resumed tasks, including
T03A. Earlier records describe historical delivery order and do not override it.
Approval to implement, passing checks, or silence is not candidate acceptance.

W07 records this workflow on the existing branch. The user separately approved
publishing the earlier documentation on `feat/sla-report`; see the
[publication checkpoint](tasks/W07.md#approved-publication-checkpoint-for-existing-work).
This exception does not approve a future task branch, PR, or merge.

The goal is behavior the candidate can explain in an interview. Do not claim
understanding on the candidate's behalf or turn review into a memorization test.

## Task proposal and completion record

Keep a concrete proposal here while it awaits execution. Once work has been
performed, move its detailed record to `tasks/<ID>.md` and retain a linked status
summary in the task index. Update the record and index together on review or
acceptance. Do not pre-fill speculative technical decisions for the whole roadmap.

| Field | What to record |
| --- | --- |
| ID and goal | One behavior or tightly related unit of work |
| Dependencies | Prior tasks or unresolved conditions |
| Scope | Expected files, included work, and important boundaries |
| Git delivery | Approved branch/base, commit scope/message/timing, PR target `main`; review/acceptance before PR creation; actual branch, commit, PR URL, and separate merge approval |
| Decisions | Proposed choice, reason, relevant alternative, and cost/limitation; approval tracked separately |
| Acceptance | Observable results the candidate can review |
| Verification | Meaningful examples/checks and their scope |
| API inspection evidence | For inspection tasks: approved capture method, ignored local raw-body/output directory, request metadata, and sanitized findings; follow AGENTS's API inspection output rules |
| Estimate | Implementation plus explanation/review time; revise transparently if needed |
| Approval | User message reference and approved scope/decisions, or pending |
| Result | Actual files, walkthrough, check outcomes, and uncertainty |
| Review | Questions, revisions, and explicit user acceptance, or pending |

Statuses: `Draft` (outline), `Proposed` (concrete scope awaiting approval),
`Approved`, `In progress`, `Awaiting review`, `Done` (user accepted), `Canceled`
(explicitly canceled by the user), and `Blocked`
(a named dependency prevents progress). A failed check does not authorize a scope
expansion. Approval of this document is not blanket implementation approval.

## Draft roadmap

T01 and T02 are accepted. The user canceled T03's first attempt; PR #3 is closed,
and its branch/history are retained. The user approved the concrete T03 restart
proposal with raw-output capture; attempt 2 is explicitly accepted and Done. T04's
first documentation proposal was approved by "ừ". The revised design and review
gate were approved by the later "duyệt". The user then reported "đã review" and
explicitly accepted with "chấp nhận"; T04 is Done.
T05–T22 remain **Draft**; technical decisions and execution approval are pending.
Criteria come from the supplied specification. Explain
proposed regrouping and split further if the diff would be difficult to review.

### Preparation

| ID | Small unit of work | Acceptance / review focus |
| --- | --- | --- |
| T01 | Check environment availability | Current Docker daemon and pinned dependency evidence, distinguished from historical failures |
| T02 | Resolve environment issues if needed | Approve needed changes first; demonstrate starter build, health, and tests with limits stated |
| T03 | Inspect the practice API with an agreed request scope | Sanitized representative data and pagination observations; first-call data-change timer explained before access; future inspections retain local raw bodies/output per W08 |
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

W05, W06, W07, W08, T01, T02, and T03 attempt 2 are accepted. W01/W02/W03 still lack recorded explicit
acceptance. The earlier documentation was published as `7d84cb1` and merged into
main at `857bd68`. The user then requested "hủy T03 và bắt đầu T03 lại".
T03 attempt 1 is Canceled; PR #3 was closed without deleting its branch or commits.
The old evidence is historical, not acceptance or evidence of a new live run.

W08 was approved by "duyệt" after the revised proposal to retain raw bodies locally.
The user then explicitly accepted W08 with "chấp nhận" after its completion report;
W08 is Done. PR #4 merged the rule and ignore entry into main. The user's "duyệt"
after the concrete T03 attempt 2 proposal approves carrying the W08 records and
cancellation bookkeeping into its new main-based branch, adding capture and
offline checks, one new bounded live run, and commit/push/PR delivery. The named
stash remains as backup. See [T03 attempt 2](tasks/T03.md) for the precise budget
and evidence. Restarting T03 does not reset upstream data changes. No old raw
response reconstruction, application change, further request budget, or merge is
authorized by T03. The later, separately approved T04 proposal is recorded below.

Attempt 2 completed one 11-GET run with 11 raw bodies, request metadata, and
sanitized output retained locally. Its request budget is consumed; do not rerun
the script for context or validation. PR #5 was subsequently observed merged.
The user requested recording the
offline review findings; see the task record for confirmed repeated feed sequences,
payload timing, and coverage limits, then explicitly requested "đẩy lên và chốt t03".
T03 attempt 2 is Done. The four-file records were committed with the approved
message and pushed on its task branch; follow-up PR #6 targets main.
PR #6 was subsequently observed merged as f782423. See the T03 record for earlier
delivery evidence. The user requested the next task and approved the concrete
T04 proposal with "ừ". See [T04](tasks/T04.md) and [architecture](../architecture.md)
for the original design checkpoint, Git delivery, and review points.
At the original checkpoint T04 was Awaiting review; no application implementation
or T04 PR merge was authorized.
The user later requested "bỏ pr t04"; PR #7 is CLOSED, with branch/commits retained.
This does not cancel or accept T04. The user reported insufficient feed history;
the request/event bootstrap revision initially awaited approval. T03A is deferred and
its uncommitted records are preserved in the named stash recorded in STATE.
The user then confirmed the feed lacks full history, requested inspection of local
evidence, and left other questions open. The two retained feed pages remain
unfinished; they do not independently prove historical coverage. The original
feed-only design is superseded, with the distinction recorded in architecture
and T04. The user then requested a revised T04 proposal plus a PR-after-review
rule, and approved that concrete six-file proposal with "duyệt". The current
design uses requests/events for baseline data and the feed for updates, leaving
the other questions open. No additional live inspection is authorized. The user
subsequently reported "đã review" and explicitly accepted with "chấp nhận". T04
is Done; its approved commit/push and replacement PR can now proceed. PR #7 stays
closed; merge needs separate approval. T03A stays deferred and T05 still needs
its own proposal.
