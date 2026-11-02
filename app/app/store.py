"""One atomic snapshot; calculations receive a private copy."""
from copy import deepcopy
from threading import RLock


class Store:
    def __init__(self):
        self.lock = RLock()
        self.snapshot = None
        self.coverage = None

    def get(self, first, last):
        with self.lock:
            if self.coverage and self.coverage[0] <= first <= last <= self.coverage[1]:
                return deepcopy(self.snapshot)
        return None

    def publish(self, snapshot, first, last):
        copied = deepcopy(snapshot)
        with self.lock:
            self.snapshot, self.coverage = copied, (first,last)
