from limiter import Limiter

class Buff(object):
    def __init__(self, entity, duration=5000):
        self.entity = entity
        self.duration = duration

        if self.can_apply():
            self.applied = True
            self.apply()
            self.limiter = Limiter(self.duration, skip_first=True)
        else:
            self.applied = False

    def can_apply(self):
        return True

    @property
    def elapsed(self):
        if self.limiter.is_ready():
            self.complete()
            return True

        return False

    def apply(self):
        pass

    def complete(self):
        pass

class Slow(Buff):
    def can_apply(self):
        return hasattr(self.entity, 'move')

    def apply(self):
        self.entity.set_movement_speed(self.entity.movement_speed * 4)

    def complete(self):
        self.entity.set_movement_speed(self.entity.stats['movement_speed'])

class Haste(Slow):
    def apply(self):
        self.entity.set_movement_speed(self.entity.movement_speed / 4)