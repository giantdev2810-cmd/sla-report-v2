"""Private inspection evidence; storage failures propagate before another GET."""
import json
from datetime import datetime, timezone
from pathlib import Path


class Capture:
    def __init__(self, directory):
        self.directory = Path(directory)
        self.directory.mkdir(parents=True, exist_ok=False)
        self.metadata = self.directory / "metadata.jsonl"
        self.output = self.directory / "output.jsonl"
        self.metadata.touch()
        self.output.touch()

    def append(self, path, item):
        with path.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(item) + "\n")

    def record(self, number, endpoint, params, requested, response=None, error=None):
        filename = None
        if response is not None:
            filename = f"{number:05d}.body"
            body = response.content
            if (self.directory / filename).write_bytes(body) != len(body):
                raise OSError("Incomplete body write")
        self.append(self.metadata, dict(attempt=number, endpoint=endpoint, params=params,
                    requested_utc=requested, completed_utc=datetime.now(timezone.utc).isoformat(),
                    status=response.status_code if response is not None else None,
                    raw_body=filename, error=error))

    def emit(self, **item):
        self.append(self.output, item)
