import operator
import threading
import time
from itertools import starmap


class Metric:
    def __init__(self, name, func, interval=1):
        self.name = name
        self.func = func
        self.values = []
        self._running = False
        self.interval = interval
        self.t = None

    def start_collect(self):
        self.t = threading.Thread(name=self.name, target=self._run, daemon=True)
        self._running = True
        self.t.start()

    def stop_collect(self):
        self._running = False

    def _run(self):
        while self._running:
            self.values.append(self.func())
            time.sleep(self.interval)

    def cleanup(self):
        self.values = []

    def get_current_state(self):
        return self.name, self.values


def count_moves(pos):
    return sum(starmap(operator.eq, zip(pos, pos[1:])))
