from datetime import datetime, timedelta

def topsort(graph):
    no_dep = {value for value in graph.values() if value is not None} - set(graph.keys())

    graph.update({item: set() for item in no_dep})

    while True:
        fulfilled = {item for item, deps in graph.items() if not deps}

        if not fulfilled:
            break

        for item in fulfilled:
            yield item

        graph = {item: {dep} - fulfilled if dep else set() for item, dep in graph.items() if item not in fulfilled}

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