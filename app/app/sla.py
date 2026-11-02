"""Pure SLA rules, independent of HTTP and data acquisition."""

from typing import Any
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo


def eligible_events(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Return a new list excluding reverting and referenced events for one request.

    Input events must have integer id and integer-or-null reverts_id fields.
    Retained dictionaries and their order are preserved; input is not mutated.
    This filter does not validate schemas or establish history completeness.
    """
    # Reverting a reversal does not restore its target, so inspect every reference.
    reverted_ids = {
        event["reverts_id"] for event in events if event["reverts_id"] is not None
    }
    return [
        event
        for event in events
        if event["reverts_id"] is None and event["id"] not in reverted_ids
    ]


def instant(value):
    """Parse an aware upstream timestamp into UTC."""
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("Timezone required")
    return parsed.astimezone(timezone.utc)


def local_instant(value, zone):
    """Reject wall times with no unique UTC interpretation."""
    candidates = set()
    for fold in (0, 1):
        candidate = value.replace(tzinfo=zone, fold=fold).astimezone(timezone.utc)
        if candidate.astimezone(zone).replace(tzinfo=None) == value:
            candidates.add(candidate)
    if len(candidates) != 1:
        raise ValueError("Ambiguous or nonexistent local time")
    return candidates.pop()


def business_minutes(start, end, site, holidays):
    """Union site work intervals, subtract local holidays, and floor elapsed seconds once."""
    if end <= start:
        return 0
    zone = ZoneInfo(site["timezone"])
    first = start.astimezone(zone).date() - timedelta(days=1)
    last = end.astimezone(zone).date()
    windows = []
    day = first
    while day <= last:
        hours = site["business_hours"][day.strftime("%a").lower()]
        if hours is not None:
            opening = datetime.combine(day, datetime.strptime(hours["open"], "%H:%M").time())
            closing = datetime.combine(day, datetime.strptime(hours["close"], "%H:%M").time())
            if closing <= opening:
                closing += timedelta(days=1)
            # Split overnight work so a holiday excludes only its own local date.
            part = opening
            while part < closing:
                boundary = datetime.combine(part.date() + timedelta(days=1), datetime.min.time())
                stop = min(closing, boundary)
                if part.date() not in holidays:
                    left = max(start, local_instant(part, zone))
                    right = min(end, local_instant(stop, zone))
                    if left < right:
                        windows.append((left, right))
                part = stop
        day += timedelta(days=1)
    seconds = 0
    previous_end = start
    # Union intervals rather than double-count overlapping shifts.
    for left, right in sorted(windows):
        left = max(left, previous_end)
        if right > left:
            seconds += (right - left).total_seconds()
            previous_end = right
    return int(seconds // 60)


def request_in_range(request, site, first, last):
    """Apply inclusive site-local creation dates and rule-1 exclusions."""
    day = instant(request["created_at"]).astimezone(ZoneInfo(site["timezone"])).date()
    return (first <= day <= last and request["status"] != "canceled"
            and request["deleted_at"] is None and request["merged_into_id"] is None)


def calculate_row(request, events, site, holidays, staff):
    """Calculate contract fields from one request and its complete acquired event history."""
    events = sorted(eligible_events(events), key=lambda event: (event["at"], event["id"]))
    responses = [e for e in events if e["status"] == "processing" and e["actor_id"] is not None]
    row = dict(id=request["id"], site_id=request["site_id"], responder_id=None,
               responder=None, response_business_minutes=None, within_target=None,
               completed_late=None)
    if responses:
        response = responses[0]
        minutes = business_minutes(instant(request["created_at"]),
                    datetime.fromtimestamp(response["at"], timezone.utc), site, holidays)
        target = {"High": 60, "Medium": 240, "Low": 480, None: 480}[request["priority"]]
        row.update(responder_id=response["actor_id"], responder=staff[response["actor_id"]]["name"],
                   response_business_minutes=minutes, within_target=minutes <= target)
    completions = [e for e in events if e["status"] == "complete"]
    deadlines = [e for e in events if e["due_at"] is not None]
    if completions and deadlines:
        deadline = local_instant(datetime.strptime(deadlines[-1]["due_at"], "%d/%m/%Y %H:%M"),
                                 ZoneInfo(site["timezone"]))
        row["completed_late"] = datetime.fromtimestamp(completions[-1]["at"], timezone.utc) > deadline
    return row
