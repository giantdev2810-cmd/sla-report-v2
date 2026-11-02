from fastapi.testclient import TestClient
import pytest
from app import main
from app.helpdesk import LoadError
from app.report import build_report
from test_report import snapshot

@pytest.mark.parametrize("query",["","from=2026-10-01","from=x&to=y","from=2026-10-07&to=2026-10-06","from=2026-10-01&from=2026-10-02&to=2026-10-03"])
def test_invalid_dates(query):
    assert TestClient(main.app).get("/api/sla-report?"+query).status_code==400

def test_report_contract(monkeypatch):
    class Service:
        def report(self,first,last): return build_report(snapshot(),first,last)
    monkeypatch.setattr(main,"service",Service())
    response=TestClient(main.app).get("/api/sla-report?from=2026-10-06&to=2026-10-06")
    assert response.status_code==200
    assert set(response.json())=={"from","to","requests","responders"}

def test_safe_error(monkeypatch):
    class Service:
        def report(self,*args): raise LoadError("load_budget")
    monkeypatch.setattr(main,"service",Service())
    assert TestClient(main.app).get("/api/sla-report?from=2026-10-06&to=2026-10-06").json()=={"error":"load_budget"}
