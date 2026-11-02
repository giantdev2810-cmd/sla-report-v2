"""Build contract output from one consistent acquired snapshot."""
from datetime import datetime
from .sla import request_in_range, calculate_row


def build_report(snapshot, first, last):
    rows = []
    for request in snapshot["requests"].values():
        site = snapshot["sites"][request["site_id"]]
        if request_in_range(request, site, first, last):
            holidays = {datetime.strptime(h["date"], "%d/%m/%Y").date()
                        for h in snapshot["holidays"][site["id"]]}
            rows.append(calculate_row(request, snapshot["events"][request["id"]],
                                      site, holidays, snapshot["staff"]))
    responders = {}
    for row in rows:
        if row["responder_id"] is None:
            continue
        group = responders.setdefault(row["responder_id"], dict(id=row["responder_id"],
                    name=row["responder"], requests=0, within_target=0, completed_late=0))
        group["requests"] += 1
        group["within_target"] += row["within_target"] is True
        group["completed_late"] += row["completed_late"] is True
    return {"from":first.isoformat(), "to":last.isoformat(), "requests":sorted(rows,key=lambda r:r["id"]),
            "responders":sorted(responders.values(),key=lambda r:r["id"])}
