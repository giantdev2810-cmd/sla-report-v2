"""On-demand baseline loading. No feed or automatic refresh in the MVP."""
import math
from threading import Lock
from .helpdesk import HelpdeskClient, LoadError
from .sla import instant, request_in_range
from .report import build_report
from .store import Store


def rows(payload):
    data = payload["data"]
    if not isinstance(data,list) or any(not isinstance(row,dict) for row in data):
        raise ValueError("Invalid rows")
    return data


def keyed(data):
    result = {}
    for item in data:
        if type(item["id"]) is not int:
            raise ValueError("Integer ID required")
        if item["id"] in result and result[item["id"]] != item:
            raise ValueError("Conflicting identity")
        result[item["id"]] = item
    return result


def walk_requests(client):
    result, page, final = {}, 1, 1
    previous = None
    while page <= final:
        payload = client.get("/v1/requests", {"page":page,"per_page":100})
        if type(payload["total_pages"]) is not int or payload["total_pages"] < 1:
            raise ValueError("Invalid page count")
        if type(payload["page"]) is not int or payload["page"] != page:
            raise ValueError("Invalid page response")
        final = max(final,payload["total_pages"])
        data = rows(payload)
        if data and data == previous:
            raise LoadError("pagination_no_progress")
        previous = data
        if not data and page < final:
            raise LoadError("incomplete_requests")
        for item in data:
            if type(item["id"]) is not int:
                raise ValueError("Integer ID required")
            version = instant(item["updated_at"])
            old = result.get(item["id"])
            if old and instant(old["updated_at"]) == version and old != item:
                raise ValueError("Version conflict")
            if old is None or instant(old["updated_at"]) < version:
                result[item["id"]] = item
        page += 1
    return result


def selected(requests, sites, first, last):
    result = {}
    for key, item in requests.items():
        if item["status"] not in {"pending","processing","complete","canceled"}:
            raise ValueError("Invalid status")
        if item["priority"] not in {None,"High","Medium","Low"}:
            raise ValueError("Invalid priority")
        if type(item["site_id"]) is not int:
            raise ValueError("Invalid site")
        if request_in_range(item, sites[item["site_id"]],first,last):
            result[key] = item
    return result


def walk_events(client, request_id):
    events, page, previous = {}, 1, None
    while True:
        payload = client.get(f"/v1/requests/{request_id}/events", {"page":page})
        if type(payload["has_more"]) is not bool or payload["page"] != page:
            raise ValueError("Invalid event pagination")
        data = rows(payload)
        if payload["has_more"] and (not data or data == previous):
            raise LoadError("event_no_progress")
        previous = data
        for key,event in keyed(data).items():
            if key in events and events[key] != event:
                raise ValueError("Event conflict")
            if type(event["at"]) is not int or not math.isfinite(event["at"]):
                raise ValueError("Invalid event time")
            if event["reverts_id"] is not None and type(event["reverts_id"]) is not int:
                raise ValueError("Invalid reversal")
            if event["status"] not in {"pending","processing","complete","canceled"}:
                raise ValueError("Invalid event status")
            if event["actor_id"] is not None and type(event["actor_id"]) is not int:
                raise ValueError("Invalid actor")
            events[key] = event
        if not payload["has_more"]:
            break
        page += 1
    if any(e["reverts_id"] is not None and e["reverts_id"] not in events for e in events.values()):
        raise ValueError("Missing event reference")
    return list(events.values())


def acquire(client, first, last):
    sites = keyed(rows(client.get("/v1/sites")))
    staff = keyed(rows(client.get("/v1/staff")))
    holidays = {key:rows(client.get(f"/v1/sites/{key}/holidays")) for key in sites}
    initial = selected(walk_requests(client),sites,first,last)
    current = selected(walk_requests(client),sites,first,last)
    if initial != current:
        raise LoadError("requests_changed")
    events = {key:walk_events(client,key) for key in current}
    final = selected(walk_requests(client),sites,first,last)
    if current != final:
        raise LoadError("requests_changed")
    snapshot = dict(sites=sites,staff=staff,holidays=holidays,requests=final,events=events)
    # Validate calculations before publishing any part of the load.
    build_report(snapshot,first,last)
    return snapshot


class ReportService:
    def __init__(self, client_factory=HelpdeskClient):
        self.store, self.load_lock = Store(), Lock()
        self.client_factory = client_factory

    def report(self,first,last):
        with self.load_lock:
            snapshot = self.store.get(first,last)
            if snapshot is None:
                try:
                    client = self.client_factory()
                except OSError:
                    raise LoadError("capture_storage") from None
                try:
                    snapshot = acquire(client,first,last)
                    if client.capture:
                        client.capture.emit(result="complete",attempts=client.attempts)
                    self.store.publish(snapshot,first,last)
                except OSError:
                    if client.capture:
                        try:
                            client.capture.emit(result="failed", attempts=client.attempts,
                                                error="capture_storage")
                        except OSError:
                            pass  # The HTTP error remains the safe fallback if storage is unavailable.
                    raise LoadError("capture_storage") from None
                except (LoadError,ValueError,KeyError,TypeError,OverflowError) as error:
                    failure = error if isinstance(error,LoadError) else LoadError("upstream_data",502)
                    if client.capture:
                        try:
                            client.capture.emit(result="failed",attempts=client.attempts,error=failure.code)
                        except OSError:
                            failure = LoadError("capture_storage")
                    raise failure from None
                finally:
                    client.close()
            return build_report(snapshot,first,last)
