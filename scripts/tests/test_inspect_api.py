"""Offline guarantees for evidence retention and bounded inspection traffic."""

import json
import subprocess

import httpx
import pytest

from scripts import inspect_api as inspector


def read_lines(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def full_sample(request):
    path = request.url.path
    page = int(request.url.params.get("page", "1"))
    if path == "/v1/sites":
        return {"data": [{"id": 11, "name": "PRIVATE_SITE"}, {"id": 12}]}
    if path.endswith("/holidays"):
        return {"data": [{"date": "10/08/2026", "name": "PRIVATE_HOLIDAY"}]}
    if path in ("/v1/staff", "/v1/statuses"):
        return {"data": [{"id": 1, "name": "PRIVATE_PERSON"}]}
    if path == "/v1/requests":
        return {"data": [{"id": page, "title": "PRIVATE_TITLE", "created_at": "2026-10-06T02:15:07Z"}],
                "page": page, "per_page": 100, "total_pages": 2}
    if path == "/v1/requests/1":
        return {"id": 1, "title": "PRIVATE_TITLE"}
    if path.endswith("/events"):
        return {"data": [{"id": page, "at": 1791874530, "actor_id": None,
                          "due_at": "07/10/2026 10:00", "note": "PRIVATE_NOTE"}],
                "has_more": page == 1}
    if path == "/v1/changes":
        return {"data": [{"seq": 1, "type": "event.created"}],
                "next_cursor": "PRIVATE_CURSOR", "has_more": "cursor" not in request.url.params}
    raise AssertionError("Unexpected endpoint")


def test_full_run_retains_all_bodies_and_forwards_cursor_without_leaking(tmp_path, capsys):
    capture = inspector.Capture(tmp_path / "run")
    bodies = []
    calls = []

    def handle(request):
        calls.append(request)
        body = json.dumps(full_sample(request), indent=2).encode() + b"\n"
        bodies.append(body)
        return httpx.Response(200, content=body)

    with httpx.Client(base_url="https://example.test", headers={"Authorization": "Bearer PRIVATE_TOKEN"},
                      transport=httpx.MockTransport(handle)) as client:
        assert inspector.run_inspection(client, capture) == 0

    assert len(calls) == 12
    assert calls[-1].url.params["cursor"] == "PRIVATE_CURSOR"
    records = read_lines(capture.metadata)
    assert len(records) == 12
    for entry, body in zip(records, bodies):
        assert (capture.directory / entry["raw_body"]).read_bytes() == body
        assert entry["bytes"] == len(body)
        assert entry["status"] == 200
        assert entry["requested_utc"] <= entry["completed_utc"]
    assert records[-1]["cursor_supplied"] is True
    assert read_lines(capture.output)[-1]["result"] == "complete"
    for text in (capture.output.read_text(), capture.metadata.read_text(), capsys.readouterr().out):
        assert "PRIVATE_" not in text


def test_thirteenth_get_is_rejected_before_transport(tmp_path):
    capture = inspector.Capture(tmp_path / "run")
    calls = []

    def handle(request):
        calls.append(request)
        return httpx.Response(200, json={"data": []})

    with httpx.Client(base_url="https://example.test", transport=httpx.MockTransport(handle)) as client:
        inspection = inspector.Inspection(client, capture)
        with pytest.raises(ValueError, match="budget exhausted"):
            for _ in range(13):
                inspection.get("sites", "/v1/sites")
    assert len(calls) == 12


@pytest.mark.parametrize("status,body", [
    (429, b'{"error": "PRIVATE_ERROR"}\n'),
    (500, b"<html>PRIVATE_ERROR</html>\r\n"),
    (200, b"{ invalid JSON PRIVATE_ERROR\r\n"),
])
def test_http_and_json_errors_retain_original_body_and_stop(tmp_path, capsys, status, body):
    capture = inspector.Capture(tmp_path / "run")
    calls = []

    def handle(request):
        calls.append(request)
        return httpx.Response(status, content=body, headers={"Retry-After": "30"})

    with httpx.Client(base_url="https://example.test", transport=httpx.MockTransport(handle)) as client:
        assert inspector.run_inspection(client, capture) == 1
    assert len(calls) == 1
    record, = read_lines(capture.metadata)
    assert record["status"] == status
    assert (capture.directory / record["raw_body"]).read_bytes() == body
    assert read_lines(capture.output)[-1]["result"] == "stopped"
    assert "PRIVATE_" not in capsys.readouterr().out


@pytest.mark.parametrize("operation,expected_gets", [("save_body", 1), ("record", 1), ("emit", 0)])
def test_capture_failure_prevents_further_gets(tmp_path, monkeypatch, operation, expected_gets):
    capture = inspector.Capture(tmp_path / "run")
    calls = []

    def fail(*args, **kwargs):
        raise OSError("PRIVATE_DISK_ERROR")

    def handle(request):
        calls.append(request)
        return httpx.Response(200, json={"data": []})

    monkeypatch.setattr(capture, operation, fail)
    with httpx.Client(base_url="https://example.test", transport=httpx.MockTransport(handle)) as client:
        assert inspector.run_inspection(client, capture) == 1
    assert len(calls) == expected_gets


def test_transport_failure_records_no_invented_body_or_status(tmp_path, capsys):
    capture = inspector.Capture(tmp_path / "run")
    calls = []

    def handle(request):
        calls.append(request)
        raise httpx.ReadTimeout("PRIVATE_URL_OR_CURSOR")

    with httpx.Client(base_url="https://example.test", transport=httpx.MockTransport(handle)) as client:
        assert inspector.run_inspection(client, capture) == 1
    assert len(calls) == 1
    record, = read_lines(capture.metadata)
    assert record["status"] is None and record["raw_body"] is None
    assert not list(capture.directory.glob("*.body"))
    assert "PRIVATE_" not in capture.output.read_text() + capture.metadata.read_text() + capsys.readouterr().out


def test_initial_capture_failure_never_constructs_client(monkeypatch, capsys):
    monkeypatch.setenv("HELPDESK_URL", "https://example.test")
    monkeypatch.setenv("HELPDESK_TOKEN", "PRIVATE_TOKEN")

    def fail_capture():
        raise OSError("PRIVATE_PATH")

    def unexpected_client(*args, **kwargs):
        raise AssertionError("Client created before capture was ready")

    monkeypatch.setattr(inspector, "create_capture", fail_capture)
    monkeypatch.setattr(inspector.httpx, "Client", unexpected_client)
    assert inspector.main() == 1
    assert "PRIVATE_" not in capsys.readouterr().out


def test_git_ignores_private_capture_subtree():
    root = inspector.Path(inspector.__file__).resolve().parents[1]
    result = subprocess.run(["git", "check-ignore", "--quiet", "--",
                             ".local/inspect/T03/example/01-sites.body"], cwd=root)
    assert result.returncode == 0
