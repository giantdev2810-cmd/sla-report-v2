from datetime import date, datetime, timezone
import pytest
from app.sla import business_minutes, instant, calculate_row, local_instant
from zoneinfo import ZoneInfo

SITE={"id":1,"timezone":"Asia/Singapore","business_hours":{d:{"open":"08:00","close":"18:00"} for d in ("mon","tue","wed","thu","fri","sat","sun")}}
REQUEST={"id":1,"site_id":1,"created_at":"2026-10-06T00:15:00Z","priority":"High","status":"complete","deleted_at":None,"merged_into_id":None}
def event(id,status,time,actor=None,due=None,reverts=None):
    return dict(id=id,status=status,at=int(instant(time).timestamp()),actor_id=actor,due_at=due,reverts_id=reverts)

def test_complete_report_fields():
    events=[event(1,"processing","2026-10-06T01:00:00Z",7),event(2,"complete","2026-10-06T02:30:00Z",due="06/10/2026 10:00"),event(3,"pending","2026-10-06T03:00:00Z")]
    row=calculate_row(REQUEST,events,SITE,set(),{7:{"name":"Current"}})
    assert row==dict(id=1,site_id=1,responder_id=7,responder="Current",response_business_minutes=45,within_target=True,completed_late=True)

@pytest.mark.parametrize("priority,minutes,expected",[("High",60,True),("High",61,False),("Medium",240,True),("Low",480,True),(None,481,False)])
def test_targets(priority,minutes,expected):
    req={**REQUEST,"priority":priority,"created_at":"2026-10-06T00:00:00Z"}
    e=event(1,"processing",datetime.fromtimestamp(instant(req["created_at"]).timestamp()+minutes*60,timezone.utc).isoformat(),7)
    assert calculate_row(req,[e],SITE,set(),{7:{"name":"Current"}})["within_target"] is expected

def test_holiday_and_floor():
    assert business_minutes(instant("2026-10-06T00:00:30Z"),instant("2026-10-07T00:01:00Z"),SITE,{date(2026,10,6)})==1
    assert business_minutes(instant("2026-10-06T00:00:30Z"),instant("2026-10-06T00:01:00Z"),SITE,set())==0

def test_null_and_early_response():
    row=calculate_row(REQUEST,[],SITE,set(),{})
    assert all(row[k] is None for k in ("responder_id","responder","response_business_minutes","within_target","completed_late"))
    e=event(1,"processing","2026-10-06T00:00:00Z",7)
    assert calculate_row(REQUEST,[e],SITE,set(),{7:{"name":"Current"}})["response_business_minutes"]==0

def test_overnight_holiday():
    site={**SITE,"business_hours":{d:{"open":"22:00","close":"06:00"} for d in SITE["business_hours"]}}
    assert business_minutes(instant("2026-10-06T14:00:00Z"),instant("2026-10-06T22:00:00Z"),site,{date(2026,10,7)})==120

def test_dst_rejects_ambiguous_deadline():
    with pytest.raises(ValueError):
        local_instant(datetime(2026,4,5,2,30),ZoneInfo("Australia/Sydney"))


def test_latest_deadline_and_equal_completion_not_late():
    events=[event(1,"complete","2026-10-06T02:00:00Z",due="06/10/2026 09:00"),event(2,"pending","2026-10-06T03:00:00Z",due="06/10/2026 10:00")]
    assert calculate_row(REQUEST,events,SITE,set(),{})["completed_late"] is False

def test_tied_response_uses_lowest_id_and_ignores_system():
    events=[event(9,"processing","2026-10-06T01:00:00Z",8),event(2,"processing","2026-10-06T01:00:00Z",7),event(1,"processing","2026-10-06T00:30:00Z")]
    assert calculate_row(REQUEST,events,SITE,set(),{7:{"name":"Chosen"},8:{"name":"Other"}})["responder_id"]==7

def test_seconds_sum_before_floor_and_weekend_closed():
    start,end=instant("2026-10-06T09:59:30Z"),instant("2026-10-07T00:00:30Z")
    assert business_minutes(start,end,SITE,set())==1
    site={**SITE,"business_hours":{**SITE["business_hours"],"sun":None}}
    assert business_minutes(instant("2026-10-04T00:00:00Z"),instant("2026-10-04T10:00:00Z"),site,set())==0

def test_dst_elapsed_seconds():
    site={"timezone":"Australia/Sydney","business_hours":{d:{"open":"00:00","close":"04:00"} for d in SITE["business_hours"]}}
    assert business_minutes(instant("2026-04-04T13:00:00Z"),instant("2026-04-04T18:00:00Z"),site,set())==300
