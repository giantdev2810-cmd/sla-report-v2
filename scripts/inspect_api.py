"""Inspect a bounded live sample and retain private response bodies for review.

Set HELPDESK_URL and HELPDESK_TOKEN in the process environment before running.
Capture lives under the Git-ignored .local/inspect/T03/ directory. The script
stops on the first error and makes at most twelve GET attempts without retries.
Restarting this script does not reset the upstream data-change timer.
"""

import json
import os
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import httpx


MAX_GETS = 12


def utc_now():
    return datetime.now(timezone.utc).isoformat()


class Capture:
    """Save raw bodies separately from safe summaries and request metadata.

    Writes are synchronous and propagate errors so no later GET can proceed
    after evidence storage fails. The caller must verify Git ignores directory.
    """

    def __init__(self, directory):
        self.directory = Path(directory)
        self.directory.mkdir(parents=True, exist_ok=False)
        self.output = self.directory / "output.jsonl"
        self.metadata = self.directory / "metadata.jsonl"
        self.output.touch(exist_ok=False)
        self.metadata.touch(exist_ok=False)

    @staticmethod
    def append(path, entry):
        with path.open("a", encoding="utf-8", newline="\n") as stream:
            stream.write(json.dumps(entry, sort_keys=True) + "\n")

    def emit(self, **summary):
        self.append(self.output, summary)
        print(json.dumps(summary, sort_keys=True), flush=True)

    def record(self, **metadata):
        self.append(self.metadata, metadata)

    def save_body(self, filename, body):
        if (self.directory / filename).write_bytes(body) != len(body):
            raise OSError("Incomplete response body write")


def create_capture():
    root = Path(__file__).resolve().parents[1]
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    directory = root / ".local" / "inspect" / "T03" / timestamp
    ignored = subprocess.run(
        ["git", "check-ignore", "--quiet", "--", str(directory / "metadata.jsonl")],
        cwd=root, capture_output=True,
    )
    if ignored.returncode != 0:
        raise OSError("Inspection directory must be ignored by Git")
    return Capture(directory)


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
    def __init__(self, client, capture):
        self.client = client
        self.capture = capture
        self.attempts = 0

    def get(self, label, path, params=None):
        if self.attempts >= MAX_GETS:
            raise ValueError("request budget exhausted")
        self.capture.emit(attempt=self.attempts + 1, endpoint=label)
        self.attempts += 1
        # Cursor values belong only in raw response files, never in metadata.
        safe_params = {key: value for key, value in (params or {}).items()
                       if key in {"page", "per_page", "limit"}}
        metadata = dict(attempt=self.attempts, requested_utc=utc_now(), endpoint=path,
                        params=safe_params, cursor_supplied="cursor" in (params or {}))
        try:
            response = self.client.get(path, params=params)
        except httpx.HTTPError as error:
            self.capture.record(**metadata, completed_utc=utc_now(), status=None,
                                raw_body=None, error=type(error).__name__)
            raise
        filename = f"{self.attempts:02d}-{label}.body"
        # Save the body before status/JSON checks so error responses survive too.
        self.capture.save_body(filename, response.content)
        self.capture.record(**metadata, completed_utc=utc_now(), status=response.status_code,
                            raw_body=filename, bytes=len(response.content))
        # Do not raise HTTPStatusError: its URL may contain a change cursor.
        if response.status_code != 200:
            self.capture.emit(error="http_status", status=response.status_code)
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
        self.capture.emit(**summary)
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
            self.capture.emit(holiday_dates_ddmmyyyy=all(
                matches_format(row.get("date"), "%d/%m/%Y") for row in holidays
            ), holiday_sample_size=len(holidays))

        requests = self.rows("requests_page_1", "/v1/requests", {"page": 1, "per_page": 100})
        first_rows = requests["data"]
        self.capture.emit(request_created_at_utc=all(
            matches_format(row.get("created_at"), "%Y-%m-%dT%H:%M:%SZ")
            for row in first_rows
        ), request_sample_size=len(first_rows))
        if requests.get("total_pages", 0) > 1:
            second = self.rows("requests_page_2", "/v1/requests", {"page": 2, "per_page": 100})
            first_ids = {row.get("id") for row in first_rows}
            self.capture.emit(request_page_overlap=len(first_ids & {row.get("id") for row in second["data"]}))
        if first_rows:
            request_id = first_rows[0].get("id")
            if type(request_id) is not int:
                raise ValueError("expected integer request ID")
            detail = self.get("request_detail", f"/v1/requests/{request_id}")
            self.capture.emit(detail_fields=shape(detail))
            events = self.rows("events_page_1", f"/v1/requests/{request_id}/events", {"page": 1})
            self.event_summary(events["data"])
            if events.get("has_more") is True:
                second = self.rows("events_page_2", f"/v1/requests/{request_id}/events", {"page": 2})
                self.event_summary(second["data"])
                event_ids = {row.get("id") for row in events["data"]}
                self.capture.emit(event_page_overlap=len(event_ids & {row.get("id") for row in second["data"]}))

        changes = self.rows("changes_page_1", "/v1/changes", {"limit": 5})
        self.change_summary(changes["data"])
        if changes.get("has_more") is True:
            cursor = changes.get("next_cursor")
            if not isinstance(cursor, str) or not cursor:
                raise ValueError("missing next cursor")
            second = self.rows("changes_page_2", "/v1/changes", {"limit": 5, "cursor": cursor})
            self.change_summary(second["data"])

    def event_summary(self, rows):
        timestamps = [row.get("at") for row in rows]
        numeric = all(type(value) is int for value in timestamps)
        deadlines = [row["due_at"] for row in rows if row.get("due_at") is not None]
        self.capture.emit(event_sample_size=len(rows), at_integer=numeric,
             newest_first=numeric and timestamps == sorted(timestamps, reverse=True),
             system_events=sum(row.get("actor_id") is None for row in rows),
             reverting_events=sum(row.get("reverts_id") is not None for row in rows),
             deadline_count=len(deadlines),
             deadlines_local_format=all(matches_format(value, "%d/%m/%Y %H:%M") for value in deadlines))

    def change_summary(self, rows):
        allowed = {"request.created", "request.updated", "event.created", "staff.updated"}
        counts = Counter(row.get("type") if row.get("type") in allowed else "other" for row in rows)
        seq = [row.get("seq") for row in rows]
        self.capture.emit(change_types=dict(counts), seq_integer=all(type(value) is int for value in seq),
             ascending_seq=all(type(value) is int for value in seq) and seq == sorted(seq))
def run_inspection(client, capture):
    """Run one approved inspection; failures stop traversal without a retry."""
    inspection = Inspection(client, capture)
    try:
        inspection.run()
        capture.emit(result="complete", attempts=inspection.attempts, completed_utc=utc_now())
    except (httpx.HTTPError, ValueError, TypeError, KeyError, OSError):
        # Error text and URLs can contain cursor values or private response data.
        try:
            capture.emit(result="stopped", error="API or capture error",
                         attempts=inspection.attempts, completed_utc=utc_now())
        except OSError:
            print('{"result": "stopped", "error": "Cannot save final output"}', flush=True)
        return 1
    return 0


def main():
    base_url = os.environ.get("HELPDESK_URL", "").rstrip("/")
    token = os.environ.get("HELPDESK_TOKEN", "")
    if not base_url or not token:
        print('{"error": "Set HELPDESK_URL and HELPDESK_TOKEN before running"}', flush=True)
        return 1
    # Capture must be ready before constructing a client or making a live call.
    try:
        capture = create_capture()
        capture.emit(started_utc=utc_now(), max_gets=MAX_GETS,
                     capture_directory=str(capture.directory.relative_to(Path(__file__).resolve().parents[1])),
                     warning="Restarting inspection does not reset upstream data changes")
        with httpx.Client(base_url=base_url, headers={"Authorization": f"Bearer {token}"},
                          timeout=10.0, follow_redirects=False) as client:
            return run_inspection(client, capture)
    except (OSError, httpx.HTTPError, ValueError):
        print('{"result": "stopped", "error": "Cannot initialize capture or client"}', flush=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
