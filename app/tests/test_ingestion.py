from copy import deepcopy
from datetime import date
import httpx
import pytest
from app.helpdesk import HelpdeskClient, LoadError
from app.ingestion import ReportService
from test_sla_rules import SITE, REQUEST, event

FIRST=LAST=date(2026,10,6)
class Clock:
    def __init__(self): self.now=0
    def __call__(self): return self.now
    def sleep(self,n): self.now+=n

def make_client(handler,**kwargs):
    clock=Clock()
    return HelpdeskClient("https://example.test","PRIVATE_TOKEN",transport=httpx.MockTransport(handler),clock=clock,sleep=clock.sleep,**kwargs)

def sample(request):
    path=request.url.path
    if path=="/v1/sites": data={"data":[SITE]}
    elif path=="/v1/staff": data={"data":[{"id":7,"name":"Current"}]}
    elif path.endswith("/holidays"): data={"data":[]}
    elif path=="/v1/requests": data={"data":[{**REQUEST,"updated_at":REQUEST["created_at"]}],"page":1,"total_pages":1}
    else: data={"data":[event(1,"processing","2026-10-06T01:00:00Z",7)],"page":1,"has_more":False}
    return httpx.Response(200,json=data)

def test_full_load_and_subrange_cache():
    calls=[]
    def handler(request): calls.append(request.url.path); return sample(request)
    service=ReportService(lambda:make_client(handler))
    report=service.report(FIRST,LAST)
    assert report["requests"][0]["response_business_minutes"]==45
    assert calls.count("/v1/requests")==3
    assert service.report(FIRST,LAST)==report
    assert len(calls)==7
    private=service.store.get(FIRST,LAST)
    private["requests"].clear()
    assert service.report(FIRST,LAST)==report

def test_changing_request_never_publishes():
    count=0
    def handler(request):
        nonlocal count
        response=sample(request)
        if request.url.path=="/v1/requests":
            count+=1
            payload=response.json();payload["data"][0]["priority"]="Low" if count>1 else "High"
            return httpx.Response(200,json=payload)
        return response
    service=ReportService(lambda:make_client(handler))
    with pytest.raises(LoadError,match="requests_changed"):service.report(FIRST,LAST)
    assert service.store.snapshot is None

@pytest.mark.parametrize("status",[500,502,503,504,429])
def test_retries_are_bounded(status):
    calls=[]
    def handler(request):
        calls.append(request)
        return httpx.Response(status,json={"error":"PRIVATE"},headers={"Retry-After":"2"})
    client=make_client(handler)
    with pytest.raises(LoadError):client.get("/v1/sites")
    assert len(calls)==3
    client.close()

def test_attempt_budget_counts_retries():
    calls=[]
    def handler(request): calls.append(request);return httpx.Response(500)
    client=make_client(handler,max_gets=1)
    with pytest.raises(LoadError,match="budget"):client.get("/v1/sites")
    assert len(calls)==1
    client.close()

@pytest.mark.parametrize("header",[None,"bad","nan","-1","999999"])
def test_invalid_or_over_budget_retry_after_stops(header):
    calls=[]
    def handler(request):
        calls.append(request)
        return httpx.Response(429,headers={} if header is None else {"Retry-After":header})
    client=make_client(handler)
    with pytest.raises(LoadError):client.get("/v1/sites")
    assert len(calls)==1
    client.close()

def test_transport_failure_retries_three_times():
    calls=[]
    def handler(request):calls.append(request);raise httpx.ReadTimeout("PRIVATE")
    client=make_client(handler)
    with pytest.raises(LoadError,match="transport"):client.get("/v1/sites")
    assert len(calls)==3
    client.close()


def test_overlapping_request_and_event_pages():
    calls=[]
    def handler(request):
        calls.append(request)
        if request.url.path=="/v1/requests":
            payload=sample(request).json()
            payload.update(page=int(request.url.params["page"]),total_pages=2,total=1)
            # Same ID is repeated across pages, with different envelope metadata.
            if payload["page"]==2:payload["data"].append({**payload["data"][0],"id":2})
            return httpx.Response(200,json=payload)
        if request.url.path.endswith("/events"):
            page=int(request.url.params["page"])
            return httpx.Response(200,json={"page":page,"has_more":page==1,"data":[event(page,"processing","2026-10-06T01:00:00Z",7)]})
        return sample(request)
    service=ReportService(lambda:make_client(handler))
    result=service.report(FIRST,LAST)
    assert len(result["requests"])==2
    assert result["responders"][0]["requests"]==2
    assert len([r for r in calls if r.url.path=="/v1/requests"])==6

def test_conflicting_event_and_missing_reference_fail():
    for bad in [event(1,"pending","2026-10-06T01:00:00Z",reverts=999),{"id":1}]:
        def handler(request):
            if request.url.path.endswith("/events"):
                return httpx.Response(200,json={"page":1,"has_more":False,"data":[bad]})
            return sample(request)
        service=ReportService(lambda:make_client(handler))
        with pytest.raises(LoadError):service.report(FIRST,LAST)
        assert service.store.snapshot is None
