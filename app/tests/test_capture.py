import json
import httpx
import pytest
from app.capture import Capture
from test_ingestion import make_client

def test_raw_error_bytes_preserved(tmp_path):
    capture=Capture(tmp_path/"run")
    body=b"<html>PRIVATE_BODY</html>\r\n"
    client=make_client(lambda request:httpx.Response(404,content=body),capture=capture)
    with pytest.raises(Exception):client.get("/v1/sites")
    client.close()
    record=json.loads(capture.metadata.read_text())
    assert (capture.directory/record["raw_body"]).read_bytes()==body
    assert record["status"]==404
    assert "PRIVATE" not in capture.metadata.read_text()

def test_write_failure_stops_before_another_get(tmp_path,monkeypatch):
    capture=Capture(tmp_path/"run");calls=[]
    def fail(*args):raise OSError("disk")
    monkeypatch.setattr(capture,"record",fail)
    def handler(request):calls.append(request);return httpx.Response(500)
    client=make_client(handler,capture=capture)
    with pytest.raises(OSError):client.get("/v1/sites")
    assert len(calls)==1
    client.close()


def test_service_records_storage_failure_without_publishing(tmp_path,monkeypatch):
    from app.ingestion import ReportService
    from app.helpdesk import LoadError
    from test_ingestion import sample,FIRST,LAST
    capture=Capture(tmp_path/"run")
    calls=[]
    def fail(*args,**kwargs):raise OSError("disk")
    monkeypatch.setattr(capture,"record",fail)
    def handler(request):calls.append(request);return sample(request)
    service=ReportService(lambda:make_client(handler,capture=capture))
    with pytest.raises(LoadError,match="capture_storage"):service.report(FIRST,LAST)
    assert len(calls)==1 and service.store.snapshot is None
    assert json.loads(capture.output.read_text())["result"]=="failed"


def test_transport_metadata_has_no_fabricated_response(tmp_path):
    capture=Capture(tmp_path/"run")
    def handler(request):raise httpx.ConnectError("PRIVATE_URL")
    client=make_client(handler,capture=capture)
    with pytest.raises(Exception):client.get("/v1/sites")
    client.close()
    records=[json.loads(line) for line in capture.metadata.read_text().splitlines()]
    assert len(records)==3 and all(row["status"] is None and row["raw_body"] is None for row in records)
    assert not list(capture.directory.glob("*.body"))
    assert "PRIVATE" not in capture.metadata.read_text()
