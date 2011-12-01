from datetime import datetime, timedelta
from random import randint

class Timer(object):
    def __init__(self, ms=100):
        self.set_delta(ms)

    def set_delta(self, ms):
        self.delta = timedelta(milliseconds=ms)
        self.last_time = None

    def is_ready(self):
        now = datetime.now()

        if self.last_time is None or self.last_time <= now - self.delta:
            self.last_time = now
            return True

        return False