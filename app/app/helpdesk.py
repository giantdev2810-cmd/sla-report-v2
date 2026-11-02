"""Bounded synchronous HTTP acquisition with optional private inspection capture."""
import math
import os
import time
from datetime import datetime, timezone
import httpx


class LoadError(Exception):
    def __init__(self, code, status=503):
        self.code, self.status = code, status
        super().__init__(code)


class HelpdeskClient:
    def __init__(self, base_url=None, token=None, *, capture=None, transport=None,
                 max_gets=6000, max_seconds=1800, clock=time.monotonic, sleep=time.sleep):
        self.clock, self.sleep = clock, sleep
        self.deadline = clock() + max_seconds
        self.max_gets, self.attempts, self.last_start = max_gets, 0, None
        self.capture = capture
        self.client = httpx.Client(base_url=(base_url or os.environ.get("HELPDESK_URL", "http://localhost:4010")).rstrip("/"),
                    headers={"Authorization": "Bearer " + (token or os.environ.get("HELPDESK_TOKEN", "")),
                             "Accept": "application/json"}, transport=transport, follow_redirects=False)

    def close(self):
        self.client.close()

    def wait(self, seconds):
        if self.clock() + seconds >= self.deadline:
            raise LoadError("load_deadline")
        if seconds > 0:
            self.sleep(seconds)

    def get(self, path, params=None):
        for retry in range(3):
            if self.attempts >= self.max_gets or self.clock() >= self.deadline:
                raise LoadError("load_budget")
            if self.last_start is not None:
                self.wait(max(0, .25 - (self.clock() - self.last_start)))
            self.attempts += 1
            self.last_start = self.clock()
            requested = datetime.now(timezone.utc).isoformat()
            try:
                response = self.client.get(path, params=params, timeout=min(10, self.deadline-self.clock()))
            except httpx.TransportError as error:
                if self.capture:
                    self.capture.record(self.attempts,path,params or {},requested,error=type(error).__name__)
                if retry == 2:
                    raise LoadError("upstream_transport") from None
                self.wait(retry + 1)
                continue
            if self.capture:
                self.capture.record(self.attempts,path,params or {},requested,response)
            if response.status_code == 200:
                try:
                    payload = response.json()
                except ValueError:
                    raise LoadError("upstream_json",502) from None
                if not isinstance(payload,dict):
                    raise LoadError("upstream_shape",502)
                return payload
            if response.status_code == 429:
                try:
                    delay = float(response.headers["Retry-After"])
                    if not math.isfinite(delay) or delay < 0:
                        raise ValueError()
                except (KeyError,ValueError):
                    raise LoadError("invalid_retry_after") from None
            elif response.status_code in (500,502,503,504):
                delay = retry + 1
            else:
                raise LoadError("upstream_http",502)
            if retry == 2:
                raise LoadError("upstream_retry_exhausted")
            self.wait(delay)
        raise LoadError("upstream_retry_exhausted")
