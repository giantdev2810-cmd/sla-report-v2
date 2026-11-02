# T03 attempt 1 - Canceled inspection

[Plan](../PLAN.md) | [Current state](../../STATE.md)

## Approved proposal

- Goal: inspect representative shapes, timestamp formats, and pagination before
  choosing application data flow in T04. No application behavior or dependency changes.
- Approval: the user replied "duyệt" immediately after the concrete T03 proposal.
- Budget: at most 12 sequential GET attempts, with no retries; stop on the first
  error. Sites/staff/statuses: 3; holidays for at most two sites: 2; request pages:
  2; one request detail: 1; event pages for that request: 2; change pages: 2.
  Fetch second pages only when metadata says there is more data.
- Method: `scripts/inspect_api.py` uses existing httpx, with configuration in
  process memory. Print field types, counts, and relevant format/order checks;
  never print raw payloads, headers, credentials, names, titles, or cursors.
  The first upstream call starts the documented five-minute change timer.
- Trade-off: a bounded sample limits traffic and time, but cannot establish full
  dataset coverage, all edge cases, or report correctness. Bulk acquisition is T14.
- Files: the script, this record, PLAN, STATE; DECISIONS only for supported findings.
- Verification: actual attempt count, field shapes/formats, and pagination evidence;
  report discrepancies and untested cases explicitly. Offline checks precede access.
- Estimate: 15 minutes implementation/checks plus 10 minutes explanation/review.

## Git delivery

- Approved base: up-to-date `main`; branch: `chore/t03-inspect-practice-api`.
- Main fast-forwarded to `857bd68` (merged PR #2), then the task branch was created.
- Approved commit scope: the files listed above; message:
  `chore: inspect practice API with bounded requests`.
- Push the task branch and create a PR into `main`; no merge authorization.
- Implementation/evidence commit: `72651b1` (`chore: inspect practice API with
  bounded requests`), pushed with upstream tracking.
- PR: [#3](https://github.com/giantdev2810-cmd/sla-report-v2/pull/3),
  `chore/t03-inspect-practice-api` into `main`. This delivery record is included
  in a documentation checkpoint on the same branch, using the approved commit
  scope/message. Use live branch refs for the final checkpoint's hash.
- Original delivery completed; the user subsequently canceled this attempt and PR #3 was closed.

## Evidence

- Offline mock check passed: syntax; twelve-GET ceiling; cursor forwarding in
  memory; scalar-value redaction; immediate stop on 429 without retry. No network
  was used in this check. No runtime application or SLA checks were performed.
- Live inspection completed on 2026-11-02, starting at 09:10:30.690 UTC
  (16:10:30 Vietnam time). The documented first-call-plus-five-minute milestone
  is approximately 09:15:30 UTC; earlier calls by others are unknown.
- Eleven GET attempts returned 200; script exit code 0. No retry, redirect follow,
  additional probe, or full-data acquisition occurred. The unused twelfth request
  was an event page skipped because `has_more=false`; it is not a carry-over budget.
- Sites: 3; staff: 15; statuses: 4. Holiday samples for the first two sites contained
  5 and 2 rows; all sampled dates parsed as DD/MM/YYYY. Third-site holidays untested.
- Requests: pages 1 and 2 each contained 100 rows and reported page/per-page/total
  metadata. First-page created_at values all parsed as UTC ISO strings ending Z.
  First-row shapes showed a string priority on page 1 and null priority on page 2.
- Pagination surprise: one shared ID value across the two request pages. Both
  responses reported total 11986, per_page 100, total_pages 122, whereas the normal
  ceiling calculation would yield 120. Cause and behavior across all pages remain
  unknown; no deduplication or acquisition design was selected by this task.
- Request detail was a direct object, with the same first-row field/type shape as
  the selected list row. Only the first list row's request was inspected in detail.
- That request had one event: integer `at`, null `actor_id`, one `due_at` parsing as
  DD/MM/YYYY HH:MM, no reverting event, and `has_more=false`. A single event cannot
  establish meaningful ordering or event pagination coverage.
- Changes: two pages of 5 rows, cursor continuation accepted; both `has_more=true`.
  Per-page sequences were ascending integers. Sampled types totaled 5 request.created
  and 5 event.created. The feed was not drained; expiry, duplicates, current-payload
  semantics, and staff.updated were not established by this sample.

## Walkthrough and review points

With valid process configuration, the script fetches the three reference endpoints,
two holiday lists, and requests page 1. Its total_pages value enables page 2. The
script compares ID sets and outputs only the overlap count (1), not the IDs. It then
fetches one detail and event list; false has_more skips event page 2. Finally it
fetches two small change pages, forwarding next_cursor in memory without printing
it. The final summary reports 11 attempts and complete; no raw response is saved.

Review `Inspection.get` for budget/error handling and output redaction, `run` for
the bounded traversal, and the format/order summaries for their narrow meaning.
Empty-sample all() checks are vacuously true; sample sizes must be read with them.
No architecture, persistence, ingestion, refresh, calculation, or application test
claim follows from this inspection. The script must not be rerun without new API
authorization because its per-execution ceiling is not a global quota.

## Review

Canceled by the user in "hủy T03 và bắt đầu T03 lại". PR #3 is closed; its branch/commits and historical observations are retained. No acceptance was given, and no raw responses from this attempt exist. See [the replacement attempt](T03.md).
