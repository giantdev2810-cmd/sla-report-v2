from datetime import date
from app.report import build_report
from test_sla_rules import SITE, REQUEST, event

def snapshot():
    return dict(sites={1:SITE},requests={1:REQUEST},holidays={1:[]},staff={7:{"name":"Current"}},events={1:[event(1,"processing","2026-10-06T01:00:00Z",7)]})

def test_summary_and_local_date():
    data=snapshot()
    result=build_report(data,date(2026,10,6),date(2026,10,6))
    assert result["responders"]==[dict(id=7,name="Current",requests=1,within_target=1,completed_late=0)]
    data["requests"][1]={**REQUEST,"created_at":"2026-10-05T23:00:00Z"}
    assert len(build_report(data,date(2026,10,6),date(2026,10,6))["requests"])==1
    for change in ({"status":"canceled"},{"deleted_at":"2026-10-06T00:00:00Z"},{"merged_into_id":2}):
        data["requests"][1]={**REQUEST,**change}
        assert build_report(data,date(2026,10,6),date(2026,10,6))["requests"]==[]
