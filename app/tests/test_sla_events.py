"""Rule 2 examples independent of the live API and remaining SLA rules."""

from copy import deepcopy

import pytest

from app.sla import eligible_events


@pytest.mark.parametrize(
    "references, expected_ids",
    [
        ([], []),
        ([(3, None), (1, None), (2, None)], [3, 1, 2]),
        ([(1, None), (2, None), (3, 1)], [2]),
        ([(3, 1), (2, None), (1, None)], [2]),
        ([(1, None), (2, None), (3, 1), (4, 2), (5, None)], [5]),
        ([(1, None), (2, 1), (3, 1), (4, None)], [4]),
        ([(1, None), (2, 1), (3, 2)], []),
        ([(1, 99), (2, None)], [2]),
        ([(0, None), (1, 0), (2, None)], [2]),
    ],
    ids=[
        "empty",
        "no-reversals-preserves-order",
        "reversal-after-target",
        "reversal-before-target",
        "independent-pairs",
        "shared-target",
        "chain-does-not-restore-original",
        "absent-target-still-excludes-reversal",
        "zero-target-is-not-null",
    ],
)
def test_rule_2_filters_events_without_mutating_input(references, expected_ids):
    events = [{"id": event_id, "reverts_id": target} for event_id, target in references]
    original = deepcopy(events)

    result = eligible_events(events)

    assert [event["id"] for event in result] == expected_ids
    assert events == original
    assert result is not events


def test_retained_event_payloads_and_order_are_preserved():
    first = {
        "id": 9, "reverts_id": None, "status": "complete", "at": 200,
        "actor_id": None, "actor_name": "System", "assignee_name": None,
        "due_at": "06/10/2026 10:00", "note": "Synthetic completion",
    }
    second = {
        "id": 4, "reverts_id": None, "status": "processing", "at": 100,
        "actor_id": 7, "actor_name": "Synthetic actor", "assignee_name": None,
        "due_at": None, "note": None,
    }
    events = [first, {"id": 2, "reverts_id": 1}, second, {"id": 1, "reverts_id": None}]
    original = deepcopy(events)

    result = eligible_events(events)

    assert result == [original[0], original[2]]
    assert events == original
