from datetime import datetime, timedelta
from random import randint

class Limiter(object):
    def __init__(self, ms=100, randomize=False, skip_first=False):
        self.randomize = randomize
        self.set_delta(ms, skip_first)

    def set_delta(self, ms, skip_first=False):
        if self.randomize:
            ms = randint(ms * 0.5, ms * 2)

        self.delta = timedelta(milliseconds=ms)

        if skip_first:
            self.last_time = datetime.now()
        else:
            self.last_time = None

    def is_ready(self):
        now = datetime.now()

        if self.last_time is None or self.last_time <= now - self.delta:
            self.last_time = now
            return True

        return False