# Initial SLA architecture

Revised T04 design approved by the user's "duyệt" after the proposal combining
request/event acquisition and the PR-after-review workflow. This describes the
chosen direction, not implemented behavior. The candidate reported "đã review"
and explicitly accepted with "chấp nhận"; T04 is Done as a documentation task.
T05 implements only rule 2's eligible_events helper, explicitly accepted by the
candidate with "chấp nhận t05". Ingestion, storage, remaining SLA calculations, endpoints, and refresh
are not implemented beyond the starter behavior.

## Sources and evidence

The candidate confirms that the feed does not contain the full history. Therefore
the original feed-only bootstrap is superseded. Load baseline requests from
`/v1/requests` and complete event pages from `/v1/requests/{id}/events` for each
request needed for calculation. Use the feed to update the local copy rather
than reconstruct all initial history. This replacement has higher HTTP cost.

Offline review of `.local/inspect/T03/20261102T093325641343Z/` found only two
change pages: ten rows, eight distinct seq values (1-8), four distinct request
payload IDs, and has_more=true on both pages. Changes span 30 April 2026 UTC;
the two request-list pages contain 199 distinct IDs and report total=11999.
The capture is not a completed traversal, so these counts do not independently
prove that the feed omits history. Full-history insufficiency is user-reported;
the retention window and precise missing-history mechanism remain unspecified.

## Data flow

```text
Helpdesk API: requests + full event pages + sites/holidays/current staff
                                  |
                              helpdesk <--- change feed (updates)
                                  |
                              ingestion
                                  |
                                store
                                  |
                         consistent snapshot
                                  |
HTTP dates --> main --> report --> pure SLA rules --> rows + summary --> main JSON
```

- Ingestion acquires request pages and full event history for requests needed by
  the report, plus sites, every site's holidays, and current staff. The acquisition
  range and use of upstream date filters still need their own approved details.
- The same ingestion boundary later applies feed updates. Timing the feed against
  baseline loading, cursor recovery, and conflict resolution remain open; no
  before-bootstrap capture/replay algorithm is selected here.
- Reports read the local snapshot rather than issue HTTP calls per result row.
- Follow event `has_more` and feed `next_cursor`/`has_more` during their respective
  traversals. A caught-up feed does not demonstrate complete baseline history.
  Request pagination stopping and reconciliation need a separate approved strategy;
  overlap removal or matching `total` alone cannot establish no requests were missed.

## Module boundaries

Paths are under `app/app/`. main.py and helpdesk.py are the starter modules;
sla.py now contains only eligible_events for rule 2. Other modules and remaining
rules are future work requiring approved interfaces and checks.

| Module | Responsibility | Boundary |
| --- | --- | --- |
| `helpdesk.py` | HTTP transport, environment credentials, upstream responses/errors | No SLA rules or report state ownership |
| `ingestion.py` | Request/event and reference loading, feed traversal, update coordination, bootstrap/refresh state | No SLA arithmetic or endpoint formatting |
| `store.py` | In-memory entities, duplicate/version handling, consistent snapshots | No HTTP calls or business-rule decisions |
| `sla.py` | Pure rules from request, events, site calendar, and current staff | No network, shared mutable state, or framework dependency |
| `report.py` | Select included requests, assemble contract rows, aggregate those rows | One snapshot per report; no upstream calls |
| `main.py` | HTTP input validation, report invocation, contract status/body | No embedded ingestion or business-hours calculation |

## Storage and consistency

- Key requests by ID, group events by request ID/event ID, and retain sites,
  holidays, and staff. Recognize repeated change delivery using `seq`; repeats
  must not add report rows or duplicate events.
- Request payloads describe current records rather than historical state at change
  `at`. Keep version information such as `updated_at` available for the later
  update policy; arrival order and change sequence alone do not prove freshness.
  Version conflicts, including equal timestamps or repeated sequences with
  different payloads, remain open rather than silently resolved here.
- Keep event history for reversals, first response, and completion/deadline rules.
  Current status and `due_on` cannot substitute for that history. Retain exclusion
  flags so later reports can omit canceled, deleted, or merged requests.
- Reports read a consistent snapshot of requests, events, calendars, and staff;
  readers must not observe half an update. Concrete synchronization/copy mechanics
  belong in the storage implementation proposal. Snapshots add memory/copying cost.
- Initially use process-local memory and one application worker. This limits
  database work within the three-hour budget. Restart requires bootstrap again;
  multiple workers would have independent stores. SQLite was considered for
  durability but adds schema/transaction work.

## Mapping the seven rules

| Rule | Calculation responsibility |
| --- | --- |
| 1 | Inclusive site-local creation dates; exclude canceled/deleted/merged requests |
| 2 | Remove reverting and referenced events before event-based rules |
| 3 | Earliest eligible processing event with actor; current staff name |
| 4 | Site hours, timezone and holidays; sum seconds before flooring minutes; earlier response gives zero |
| 5 | Inclusive targets: High 60, Medium 240, Low/null 480 |
| 6 | Last eligible completion versus latest eligible non-null event deadline, parsed site-locally; strictly after |
| 7 | Contract nulls when response, completion, or deadline is absent |

T05's eligible_events filters a single request's event dictionaries before future
event-based calculations. It preserves retained payloads/order without mutation;
two passes and a set cost O(n) time and O(n) space. It assumes valid id/reverts_id
fields and does not validate/deduplicate input or establish complete history.
The candidate-approved chain interpretation excludes A/B/C for B->A and C->B,
without restoring A. This is recorded in DECISIONS; no endpoint uses the helper yet.

Responder counts aggregate only included result rows, using current staff from
the same snapshot rather than historical actor names.

## Synthetic walkthrough

This example is not an API observation or executed test. A request is created on
6 October 2026 at 08:15 in Asia/Singapore, with weekday hours 08:00-18:00, no
holiday, High priority, and no exclusion flags. An eligible actor enters processing
at 09:00. The last eligible completion is 10:30; the latest eligible event deadline
is 10:00 that day.

For the inclusive 6 October report, the snapshot supplies the request, full events,
calendar, and current actor name. Response time is 2700 business seconds, or 45
minutes; within_target and completed_late are true. The responder gains one request,
one within-target count and one late count. Repeated feed rows add no contribution.
Reversals must be removed before these calculations.

## Open questions and readiness limits

The user explicitly leaves the following unresolved. Listing them does not select
a policy or authorize additional implementation or API inspection.

| Question | Consequence / later review |
| --- | --- |
| Request pagination completeness while data changes | A deduplicated set may still omit requests; reconciliation strategy needs approval |
| Baseline/feed timing and consistency | Updates must not silently leave stale or mixed data; synchronization/replay strategy is open |
| Request volume, concurrency and rate limits | Per-request event calls may exceed the startup target; measure and propose limits/retries |
| Version conflicts and repeated seq with differing payloads | Define update policy before implementing ingestion |
| Events sharing the same `at` | Rules say earliest/latest but do not give a tie-breaker; do not invent one |
| Acquisition range and upstream date-filter timezone | Report inclusion must remain site-local; upstream filtering semantics are not verified |
| Missing references, malformed data, and recovery | Define whether/how to refetch, stop, or keep readiness false |
| Concrete snapshot mechanics and browse cursors | A consistent report read alone does not guarantee exactly-once browsing across requests |

- Intended readiness requires usable request/event and reference data for the full
  six-month range, with bootstrap caught up. A partial load is not ready; caught-up
  feed traversal alone does not demonstrate complete, calculable coverage.
- Implement pure rules/report with fixtures first (T05-T10), then the store and
  level 1 reference/request/event acquisition (T10A-T10D), before endpoint/UI and
  end-to-end review (T11-T13). Extend the existing data path to six months (T14),
  then readiness/performance (T15), freshness/recovery (T16), and browsing.
  See the [roadmap](plan/PLAN.md) for dependencies and open-question gates.
  This scheduling correction does not change the design or approve those tasks.
- Targets remain readiness within eight minutes, May-October under ten seconds,
  October under five seconds, and changes visible within sixty seconds. None is
  measured or achieved by this document.
- Later proposals must select HTTP client lifecycle, request limits, retry policy
  including Retry-After, cursor recovery (the API requires restarting without a
  cursor on 410), malformed/conflicting data handling, and background lifecycle.
  No retry count, polling interval, or recovery implementation is selected here.
- Browse cursor strategy needs separate approval. One consistent report snapshot
  does not guarantee exactly-once appearance across multiple browse requests.

See [rules](rules.md), [contract](contract.md), [API](api.md), and
[T03 evidence](plan/tasks/T03.md). Rule fixtures, complete-feed reconciliation,
update/replay, performance, freshness, and browsing checks remain future work.
