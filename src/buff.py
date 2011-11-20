from datetime import datetime, timedelta

class Buff(object):
    def __init__(self, entity, source=None, duration=5000):
        self.entity = entity
        self.source = source
        self.duration = duration

        if self.can_apply():
            self.applied = True
            self.apply()
            self.tick_delta = timedelta(milliseconds=1000)
            self.final_tick = datetime.now() + timedelta(milliseconds=duration)
            self.last_tick = datetime.now()
        else:
            self.applied = False

    def can_apply(self):
        return True

    @property
    def elapsed(self):
        now = datetime.now()

        if self.last_tick <= now - self.tick_delta:
            self.last_tick = now
            self.tick()

            if self.last_tick >= self.final_tick:
                self.complete()
                return True

        return False

    def tick(self):
        pass

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

class Poison(Slow):
    def tick(self):
        self.entity.damage_taken(self.source, 2)