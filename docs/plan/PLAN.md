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
| [W09](tasks/W09.md) | Align roadmap dependencies with the accepted architecture | Done |
| [W10](tasks/W10.md) | Record user-reported blank/null SLA report rows | Awaiting review |
| [T01](tasks/T01.md) | Check environment availability | Done |
| [T02](tasks/T02.md) | Install pinned dependencies and verify the starter | Done |
| [T03 attempt 1](tasks/T03-attempt-1.md) | Inspect a bounded practice API sample (canceled first attempt) | Canceled |
| [T03 attempt 2](tasks/T03.md) | Restart inspection with private raw capture | Done |
| [T03A](tasks/T03A.md) | API data audit tool | Approved — deferred by user |
| [T04](tasks/T04.md) | Choose initial data flow and module boundaries | Done |
| [T05](tasks/T05.md) | Exclude reverting and reverted events | Done |
| [M01 planning](tasks/M01.md#planning-checkpoint) | Group level 1 work into an MVP | Done |

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
T05's pure rule-2 helper was approved by "duyệt t05" and explicitly accepted
with "chấp nhận t05"; it is Done. See its task record for the chain assumption
and checks. The user subsequently approved grouping the remaining work into
M01–M04 with "duyệt, nhưng qua nhánh mới để làm". This approves the four-file
planning update, not MVP implementation. The user then replied "duyệt" to the
checked planning handoff, accepting that result. Planning is Done; M01 application
implementation was subsequently approved with "duyệt" and is In progress.
Legacy T06–T22 and T10A–T10D are retained as checklist IDs, not separately
approved implementation tasks. The user approved
W09's roadmap revision with "duyệt", then accepted the reviewed result with
"đã chấp nhận review"; W09 is Done. Acceptance does not approve the application
tasks described by the revised roadmap. T03A is deferred
by the user and is not a prerequisite for the application tasks below.
Criteria come from the supplied specification. Explain
proposed regrouping and split further if the diff would be difficult to review.

### Grouped delivery roadmap

| Package | Scope | State |
| --- | --- | --- |
| [M01](tasks/M01.md) | Level 1 report MVP: T06–T13 plus T10A–T10D; reuse accepted T05 | Planning accepted; implementation In progress |
| M02 | Six-month coverage, readiness and performance: T14–T15 | Draft |
| M03 | Live updates and recovery: T16 | Draft |
| M04 | Browse filters, sorting, cursors and UI: T17–T19 | Draft |

T20–T22 remain the delivery checklist after level-specific verification. T03A
stays deferred and is not a prerequisite for M01. Completed task history is not
renumbered or reclassified by this grouping.

M01 will be one implementation task, with one approved overall proposal, one
implementation branch and one final candidate review/PR. Its existing checklist
IDs do not each need a branch, implementation approval or PR. The overall proposal
must bundle foreseeable technical choices, files, error policies, API budget,
verification, Git scope/message and estimate including review. Grouping alone
does not approve those choices or authorize code or API calls. New decisions or
scope changes still need approval before dependent work.

| M01 checkpoint | Checklist | Observable outcome |
| --- | --- | --- |
| 1. Correct calculations | T06–T10; reuse T05 | All seven rules and responder aggregation checked against explicit synthetic expectations |
| 2. Real data integration | T10A–T10D | Store/snapshot, reference data, request pages and full required event histories connected to calculations |
| 3. Runnable application | T11–T13 | HTTP validation/output, UI, Docker run and source-to-report checks for October and 12–18 October |

Report progress and evidence at each checkpoint without requiring separate
acceptance/PR for each internal checklist item. Only the completed M01 is handed
off for final review and explicit acceptance before its approved commit/push/PR.
An internal checkpoint or passing tests does not establish MVP completion.

M01 acceptance requires a Docker-runnable page with date input, real upstream
data, contract-shaped request rows and responder totals, and seven-rule checks.
Missing/invalid/reversed dates must return 400; loading failures or unusable data
must be visible rather than silently presented as a complete report. Detailed
error policies and acquisition completeness checks still need proposal approval.
Fixtures establish rule behavior but do not substitute for real-data integration.
Do not claim complete coverage solely from deduplication or matching upstream totals.
`/ready` must remain 503 unless the contract's usable six-month condition is met;
M01 alone does not claim M02's readiness/performance or M03/M04 behavior.

### Preparation

| ID | Small unit of work | Acceptance / review focus |
| --- | --- | --- |
| T01 | Check environment availability | Current Docker daemon and pinned dependency evidence, distinguished from historical failures |
| T02 | Resolve environment issues if needed | Approve needed changes first; demonstrate starter build, health, and tests with limits stated |
| T03 | Inspect the practice API with an agreed request scope | Sanitized representative data and pagination observations; first-call data-change timer explained before access; future inspections retain local raw bodies/output per W08 |
| T04 | Choose initial data flow and module boundaries | User approves responsibilities, data access, storage if any, and costs; record chosen design in architecture.md |

### M01 checklist: level 1 report MVP

| ID | Small unit of work | Acceptance / review focus |
| --- | --- | --- |
| T05 | Exclude reversed events | Reverting and referenced events excluded from downstream rules; examples explain chosen interpretation |
| T06 | Determine request inclusion | Inclusive site-local creation dates; canceled, deleted, and merged requests excluded |
| T07 | Calculate business duration | Timezone, hours, holidays, seconds summed before flooring to minutes, and earlier-response zero case |
| T08 | Determine response fields and target result | Earliest eligible processing actor, current staff name, thresholds, and response nulls |
| T09 | Determine completed-late result | Last eligible completion, latest eligible deadline, local parsing, strict comparison, and null cases |
| T10 | Assemble rows and responder summary | Required fields/types; responder counts agree with included rows |
| T10A | Add the in-memory store and consistent snapshots | After T10: fixture-backed identity storage and consistent report reads; no live API access |
| T10B | Load sites, holidays, and current staff through the HTTP client | After T10A: reference coverage and load failures are identifiable; approve HTTP/lifecycle/error policies first |
| T10C | Acquire baseline requests for level 1 | After T10B: approve acquisition range, date-filter semantics, pagination/reconciliation and duplicate/version handling; record coverage and limits |
| T10D | Load full event histories and integrate report calculations | After T10C and T05–T10: traverse all event pages for required requests, populate the store, and connect the report to its snapshot |
| T11 | Implement report endpoint validation/output | Contract JSON and 400 for missing/invalid/reversed dates; error-handling choices approved first |
| T12 | Show the report on the starter page | Date selection, rows, summary, and understandable loading/error behavior |
| T13 | Review level 1 end to end | Candidate traces a request from source to report; rule checks and representative report results recorded |

T05–T10 can use agreed local examples before live integration. T10A then introduces
the store/snapshot boundary; T10B–T10D acquire and integrate the data required for
level 1. T11 depends on that report data path, followed by T12 and T13. T13 must
trace actual acquisition through the HTTP report, not only fixtures; record results
for October and 12–18 October and their limits. Level 1 acquisition does not imply
six-month readiness or performance. Fixtures, interfaces, libraries, file layout,
checks, error policies and live access must be included in the grouped M01
implementation proposal; unapproved new choices still pause dependent work.

The accepted architecture defines module responsibilities. These draft steps
organize implementation inside M01 without selecting unresolved ingestion policies
or changing business rules. Legacy IDs identify checklist coverage, not separate
branches/PRs. See the dependency and open-question gates below.

### M02–M04 checklist: levels 2–4, in grading order

| ID | Small unit of work | Acceptance / review focus |
| --- | --- | --- |
| T14 | Extend existing ingestion/store coverage to six months | After T13: build on T10A–T10D, verify six-month data/event/reference coverage, and assess HTTP cost, limits and performance changes |
| T15 | Add readiness and measure performance | Ready means usable data; record month/six-month timings against contract targets and any limitations |
| T16 | Apply upstream changes | Approved refresh/recovery approach; relevant changes visible within 60 seconds, including current staff names |
| T17 | Add browse filters and sorting | Contract filters, sort directions, null placement, and tie order checked |
| T18 | Add cursor pagination | Approved cursor strategy; invalid cursors rejected and continuously matching rows appear exactly once during changes |
| T19 | Add page browsing controls | Candidate can use filters/sorting/paging and explain their endpoint interaction |

These packages are outlines; use T14–T19 to trace their scope. Split internal
checkpoints further when needed for review, within an approved grouped proposal.
Do not start a later package or level automatically.

### Dependencies and open-question gates

```text
M01 (reuse T05): T06-T10 pure rules and report fixtures
  -> T10A: store/snapshot -> T10B: references -> T10C: requests
  -> T10D: full events + report integration -> T11 -> T12 -> T13
  -> M02: T14 six-month expansion -> T15 readiness/performance
  -> M03: T16 updates/recovery -> M04: T17 -> T18 -> T19
```

The questions below remain open by user instruction. Their assigned checklist IDs
identify where the grouped package proposal must obtain approval for a policy
before implementing dependent behavior. A package may perform only its approved
independent work while a question is open;
neither this table nor roadmap approval resolves it or authorizes API calls.

| Open question | Proposal/checkpoint responsible |
| --- | --- |
| Events with equal `at` and earliest/latest selection | T08/T09 |
| HTTP lifecycle, rate limits, request budget, retries and malformed responses | T10B–T10D; reassess for six-month load in T14 |
| Request pagination completeness and duplicate/version conflicts | T10C; update conflicts revisited in T16 |
| Acquisition range and upstream date-filter timezone | T10C; expand/recheck range in T14 |
| Baseline consistency and coordination with concurrent/feed changes | T10C; refresh/recovery policy in T16 |
| Missing reference or event relationships | T10B–T10D |
| Concrete consistent-snapshot mechanism | T10A |
| Feed conflicts, cursor expiry, recovery and current staff refresh | T16 |
| Consistency/exactly-once appearance across changing browse pages | T18 |

The readiness and timing targets remain unchanged in [contract](../contract.md).
Choosing a policy later must not silently turn incomplete data into a complete
report or substitute the feed for the missing baseline history.

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
is Done; approved revision commit 86d7a9c was pushed and replacement
[PR #9](https://github.com/giantdev2810-cmd/sla-report-v2/pull/9) opened into main
after acceptance. PR #7 stays closed; merge needs separate approval. T03A stays
deferred and T05 still needs its own proposal.

PR #9 was subsequently observed merged as 9c207c0. At the user's request, branch
docs/w09-review-roadmap was created from that updated main. The user approved W09
with "duyệt" after the concrete five-file proposal: insert T10A–T10D, narrow T14,
assign open-question gates, align the architecture's scheduling note, and restore
the T03A record without dropping its stash. See [W09](tasks/W09.md) for review
evidence. The user then explicitly accepted the reviewed work with
"đã chấp nhận review". W09 is Done; accepted revision 059cba7 was pushed and
[PR #10](https://github.com/giantdev2810-cmd/sla-report-v2/pull/10) opened into main
after acceptance. Merge needs separate approval. T03A stays deferred and T05
needed its own proposal at that checkpoint.

The user subsequently confirmed the non-restoring reversal-chain interpretation
and requested its DECISIONS assumption, then approved the full T05 proposal with
"duyệt t05". See [T05](tasks/T05.md): pure eligible_events helper and synthetic
tests only. After review, the user stated "tôi là người xóa chúng, chấp nhận t05",
confirming ownership of the unrelated starter deletions and accepting T05. T05
is Done; its approved seven-file commit/push/PR may now proceed. Starter deletions
remain outside this task's delivery; merge still needs separate approval.
The branch is based on main 124e14a (PR #10 observed merged). T03A stays deferred;
T06 and later tasks need separate proposals.

The user then requested a runnable, correct MVP before further expansion and
approved grouping with "duyệt, nhưng qua nhánh mới để làm". On
docs/m01-mvp-plan from updated main 93d77fe, update this plan, architecture's
scheduling note, STATE and [M01](tasks/M01.md) only. The user subsequently replied
"duyệt" to the checked planning result; planning is accepted and Done. M01's
concrete implementation proposal is now presented for approval, not implemented.
T05 delivery bookkeeping is preserved in a named stash and the user's 46 starter
deletions remain untouched/outside scope. No code, live API run or publication is
authorized by this planning approval.

The concrete M01 implementation proposal was subsequently approved with "duyệt".
Code, offline/Docker tests and the single authorized live session are in progress;
final acceptance and publication remain pending. The user will check the UI manually.

The user subsequently requested "đẩy lên remote đi", authorizing the current M01
checkpoint commit/push on docs/m01-mvp-plan before final acceptance, using the
approved message. M01 remains In progress; PR/merge and new agent live traffic
are not authorized by that publication request. User starter deletions stay out.

The user later requested "đẩy toàn bộ lên github và tạo PR", expressly authorizing
remaining notes, user-owned starter deletions, commit/push and a PR now. This
specific publication exception does not accept M01, authorize merge, publish
ignored evidence/credentials or change the general review gate for later tasks.
Full publication 9e5fb54 was pushed; [PR #12](https://github.com/giantdev2810-cmd/sla-report-v2/pull/12)
targets main. M01 remains In progress and no merge was performed.

Current documentation checkpoint: [W10](tasks/W10.md) records the candidate's
12 October report observation without claiming an independently verified cause.
The user approved the concrete W10 proposal with "duyệt". W10 is Awaiting review.
This does not accept M01 or authorize further API inspection.
The user subsequently approved the six-bullet "How I used AI" replacement with
"ừ"; the W10 documentation revision includes it and still awaits final review.
After the checked handoff, "push và tạo pr" explicitly authorizes W10 commit/push
and a PR into main now, overriding its delivery timing only. Review acceptance
is not explicit; merge remains separately gated.
