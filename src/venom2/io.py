import simplejson
import time

class Network(object):
    def __init__(self, world):
        self.world = world
        self._buffer = []

    def emit(self, event, *args):
        self._buffer.append((event, args))

    def flush(self, callback):
        if self._buffer:
            callback(simplejson.dumps({
                'timestamp': int(time.time() * 1000),
                'instructions': self._buffer,
            }))

            self._buffer = []