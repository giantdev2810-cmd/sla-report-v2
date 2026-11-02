# Initial SLA architecture

T04 design approved by the user's "ừ" after its concrete proposal. This is a
chosen direction, not implemented application behavior. T04 is documentation only
and Awaiting review. No ingestion, store, SLA calculation, or refresh exists yet.

## Data flow

```text
Helpdesk API: sites / all site holidays / current staff / changes from the start
                                  |
                              helpdesk
                                  |
                              ingestion
                                  |
                                store
                                  |
                         consistent snapshot
                                  |
HTTP dates --> main --> report --> sla --> contract rows + summary --> main JSON
```

- Bootstrap requests and events from `/v1/changes` without a cursor; load sites,
  every site's holidays, and current staff separately. Reports use the local copy
  rather than make HTTP calls per row. Later refresh uses the same ingestion boundary.
- Follow `next_cursor` until `has_more` is false. Repeated delivery is expected;
  neither page length nor an assumed sequence step proves completion.
- The API documents every change since the start. T03's two-page sample did not
  establish complete history, event coverage, or the graded date ranges. Verify
  these during integration before claiming usable coverage. If insufficient,
  propose a revised acquisition plan before implementing a fallback.
- The alternative, request pages plus per-request events, needs many calls and
  has unresolved pagination completeness given T03's overlap/count discrepancy.
  It is not the chosen primary acquisition path.

## Module boundaries

Future paths are under `app/app/`; only main.py and helpdesk.py exist today.
Each implementation task still requires approved interfaces and checks.

| Module | Responsibility | Boundary |
| --- | --- | --- |
| `helpdesk.py` | HTTP transport, environment credentials, upstream responses/errors | No SLA rules or report state ownership |
| `ingestion.py` | Reference loading, feed traversal, update coordination, bootstrap/refresh state | No SLA arithmetic or endpoint formatting |
| `store.py` | In-memory entities, duplicate/version handling, consistent snapshots | No HTTP calls or business-rule decisions |
| `sla.py` | Pure rules from request, events, site calendar, and current staff | No network, shared mutable state, or framework dependency |
| `report.py` | Select included requests, assemble contract rows, aggregate those rows | One snapshot per report; no upstream calls |
| `main.py` | HTTP input validation, report invocation, contract status/body | No embedded ingestion or business-hours calculation |

## Storage and consistency

- Key requests by ID, group events by request ID/event ID, and retain sites,
  holidays, and staff. Recognize repeated change delivery using `seq`; repeats
  must not add report rows or duplicate events.
- Request payloads describe current records rather than historical state at change
  `at`. Guard replacement using `updated_at`; arriving later or having a later
  sequence must not let an older payload replace a newer one. Exact timestamp
  ties/conflicts and repeated sequences with differing current payloads need
  explicit handling in the ingestion implementation proposal.
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

## Readiness and deferred work

- Intended readiness requires usable request/event and reference data for the full
  six-month range, with bootstrap caught up. A partial load is not ready; caught-up
  feed traversal alone does not demonstrate complete, calculable coverage.
- Implement pure rules/report first (T05-T13), acquisition/storage under its own
  integration scope (T14), readiness/performance (T15), freshness/recovery (T16),
  then browsing. This document does not approve those tasks.
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
