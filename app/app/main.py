from pathlib import Path
from datetime import date, datetime, timezone
import re
import os
from .capture import Capture
from .helpdesk import HelpdeskClient

from .ingestion import ReportService
from .helpdesk import LoadError

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse

STATIC_DIR = Path(__file__).resolve().parent.parent / "static"

app = FastAPI(title="Response-time report")
def configured_client():
    directory = os.environ.get("M01_CAPTURE_DIR")
    capture = Capture(Path(directory) / datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")) if directory else None
    if capture:
        capture.emit(result="started", max_gets=6000, max_seconds=1800)
    return HelpdeskClient(capture=capture)


service = ReportService(configured_client)


@app.get("/")
def index():
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/health")
def health():
    return {"ok": True}


@app.get("/ready")
def ready():
    # TODO: answer 200 {"ready": true} once your app can serve six-month reports (level 2).
    return JSONResponse(status_code=503, content={"ready": False})


@app.get("/api/requests")
def browse(request: Request):
    # TODO (level 4): filters, sorting and cursor pagination, see docs/contract.md.
    return JSONResponse(status_code=501, content={"error": "not implemented"})


@app.get("/api/sla-report")
def sla_report(request: Request):
    try:
        values = []
        for key in ("from", "to"):
            entries = request.query_params.getlist(key)
            if len(entries) != 1 or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", entries[0]):
                raise ValueError()
            values.append(date.fromisoformat(entries[0]))
        first, last = values
        if first > last:
            raise ValueError()
    except ValueError:
        return JSONResponse(status_code=400, content={"error":"invalid_dates"})
    try:
        return service.report(first,last)
    except LoadError as error:
        return JSONResponse(status_code=error.status,content={"error":error.code})
