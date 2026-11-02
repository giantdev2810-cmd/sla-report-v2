"""Inspect a small live API sample; print summaries without raw payloads or cursors.

Set HELPDESK_URL and HELPDESK_TOKEN in the process environment before running.
Each execution can start the upstream five-minute data-change timer. The script
stops on the first error and makes at most twelve GET attempts without retries.
"""

import json
import os
import sys
from collections import Counter
from datetime import datetime, timezone

import httpx


MAX_GETS = 12


def emit(**summary):
    print(json.dumps(summary, sort_keys=True), flush=True)


def shape(value):
    """Describe field types, omitting scalar values and arbitrary nested keys."""
    if isinstance(value, dict):
        return {key: type(item).__name__ for key, item in value.items()}
    return type(value).__name__


def matches_format(value, pattern):
    if not isinstance(value, str):
        return False
    try:
        datetime.strptime(value, pattern)
    except ValueError:
        return False
    return True


class Inspection:
    def __init__(self, client):
        self.client = client
        self.attempts = 0

    def get(self, label, path, params=None):
        if self.attempts >= MAX_GETS:
            raise ValueError("request budget exhausted")
        self.attempts += 1
        emit(attempt=self.attempts, endpoint=label)
        response = self.client.get(path, params=params)
        # Do not raise HTTPStatusError: its URL may contain a change cursor.
        if response.status_code != 200:
            emit(error="http_status", status=response.status_code)
            raise ValueError("unexpected HTTP status")
        payload = response.json()
        if not isinstance(payload, dict):
            raise ValueError("expected an object")
        if "data" in payload and not isinstance(payload["data"], list):
            raise ValueError("expected a data list")
        rows = payload.get("data")
        summary = {"endpoint": label, "envelope": shape(payload)}
        if rows is not None:
            if not all(isinstance(row, dict) for row in rows):
                raise ValueError("expected object rows")
            summary.update(rows=len(rows), first_row=shape(rows[0]) if rows else {})
        for key in ("page", "per_page", "total_pages", "total", "has_more"):
            value = payload.get(key)
            if type(value) in (int, bool):
                summary[key] = value
        emit(**summary)
        return payload

    def rows(self, label, path, params=None):
        payload = self.get(label, path, params)
        if "data" not in payload:
            raise ValueError("missing data list")
        return payload

    def run(self):
        sites = self.rows("sites", "/v1/sites")["data"]
        self.rows("staff", "/v1/staff")
        self.rows("statuses", "/v1/statuses")
        for site in sites[:2]:
            site_id = site.get("id")
            if type(site_id) is not int:
                raise ValueError("expected integer site ID")
            holidays = self.rows("holidays", f"/v1/sites/{site_id}/holidays")["data"]
            emit(holiday_dates_ddmmyyyy=all(
                matches_format(row.get("date"), "%d/%m/%Y") for row in holidays
            ), holiday_sample_size=len(holidays))

        requests = self.rows("requests_page_1", "/v1/requests", {"page": 1, "per_page": 100})
        first_rows = requests["data"]
        emit(request_created_at_utc=all(
            matches_format(row.get("created_at"), "%Y-%m-%dT%H:%M:%SZ")
            for row in first_rows
        ), request_sample_size=len(first_rows))
        if requests.get("total_pages", 0) > 1:
            second = self.rows("requests_page_2", "/v1/requests", {"page": 2, "per_page": 100})
            first_ids = {row.get("id") for row in first_rows}
            emit(request_page_overlap=len(first_ids & {row.get("id") for row in second["data"]}))
        if first_rows:
            request_id = first_rows[0].get("id")
            if type(request_id) is not int:
                raise ValueError("expected integer request ID")
            detail = self.get("request_detail", f"/v1/requests/{request_id}")
            emit(detail_fields=shape(detail))
            events = self.rows("events_page_1", f"/v1/requests/{request_id}/events", {"page": 1})
            self.event_summary(events["data"])
            if events.get("has_more") is True:
                second = self.rows("events_page_2", f"/v1/requests/{request_id}/events", {"page": 2})
                self.event_summary(second["data"])
                event_ids = {row.get("id") for row in events["data"]}
                emit(event_page_overlap=len(event_ids & {row.get("id") for row in second["data"]}))

        changes = self.rows("changes_page_1", "/v1/changes", {"limit": 5})
        self.change_summary(changes["data"])
        if changes.get("has_more") is True:
            cursor = changes.get("next_cursor")
            if not isinstance(cursor, str) or not cursor:
                raise ValueError("missing next cursor")
            second = self.rows("changes_page_2", "/v1/changes", {"limit": 5, "cursor": cursor})
            self.change_summary(second["data"])

    @staticmethod
    def event_summary(rows):
        timestamps = [row.get("at") for row in rows]
        numeric = all(type(value) is int for value in timestamps)
        deadlines = [row["due_at"] for row in rows if row.get("due_at") is not None]
        emit(event_sample_size=len(rows), at_integer=numeric,
             newest_first=numeric and timestamps == sorted(timestamps, reverse=True),
             system_events=sum(row.get("actor_id") is None for row in rows),
             reverting_events=sum(row.get("reverts_id") is not None for row in rows),
             deadline_count=len(deadlines),
             deadlines_local_format=all(matches_format(value, "%d/%m/%Y %H:%M") for value in deadlines))

    @staticmethod
    def change_summary(rows):
        allowed = {"request.created", "request.updated", "event.created", "staff.updated"}
        counts = Counter(row.get("type") if row.get("type") in allowed else "other" for row in rows)
        seq = [row.get("seq") for row in rows]
        emit(change_types=dict(counts), seq_integer=all(type(value) is int for value in seq),
             ascending_seq=all(type(value) is int for value in seq) and seq == sorted(seq))


def main():
    base_url = os.environ.get("HELPDESK_URL", "").rstrip("/")
    token = os.environ.get("HELPDESK_TOKEN", "")
    if not base_url or not token:
        emit(error="Set HELPDESK_URL and HELPDESK_TOKEN before running")
        return 1
    emit(started_utc=datetime.now(timezone.utc).isoformat(), max_gets=MAX_GETS,
         warning="Upstream changes begin five minutes after its first call")
    # Keep exceptions private: request URLs, headers and payload text can be sensitive.
    with httpx.Client(base_url=base_url, headers={"Authorization": f"Bearer {token}"},
                      timeout=10.0, follow_redirects=False) as client:
        inspection = Inspection(client)
        try:
            inspection.run()
        except (httpx.HTTPError, ValueError, TypeError, KeyError):
            emit(result="stopped", error="API transport, JSON, or shape error", attempts=inspection.attempts)
            return 1
        emit(result="complete", attempts=inspection.attempts)
    return 0


if __name__ == "__main__":
    sys.exit(main())
