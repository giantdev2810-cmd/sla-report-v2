"""Pure SLA rules, independent of HTTP and data acquisition."""

from typing import Any


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
