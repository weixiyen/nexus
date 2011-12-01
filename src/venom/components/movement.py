import venom

class Movement(venom.Component):
    def initialize(self, speed=1):
        self._map = self.entity.world.map
        self._timer = venom.utils.Timer(speed * 100.0)

        self.speed = speed
        self.queue = None

    def busy(self):
        return not not self.queue

    def ready(self):
        return self.queue and self._timer.is_ready()

    def stop(self):
        self.queue = None

    def move(self, x, y, offset=None):
        position = self.entity.position

        self.queue = self._map.find_path((position.x, position.y), (x, y))

        if offset:
            self.queue = self.queue[offset:]

    def serialize(self):
        return {
            'speed': self.speed
        }
