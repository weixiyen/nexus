from venom2.component import Component
from venom2.timer import Timer
import random

class Kind(Component):
    def initialize(self, kind=None):
        self.kind = kind or self.entity._archetype

    def __eq__(self, other):
        return self.kind == other

class Aggro(Component):
    def initialize(self, radius=0):
        self.radius = radius

class Projectile(Component):
    def initialize(self):
        self.parent = None

class Patrol(Component):
    def initialize(self, radius=0, rate=10):
        self.radius = radius
        self._timer = Timer(1000.0 * rate)

    def ready(self):
        return self._timer.is_ready()

    def next(self):
        if not hasattr(self, '_points'):
            entity = self.entity
            world = entity.world
            position = entity.position
            self._points = world.map.get_points_in_radius(position.x, position.y, self.radius)

        return random.choice(self._points)

class Attack(Component):
    def initialize(self, power=0, speed=5):
        self.power = power
        self.speed = speed
        self._timer = Timer(100.0 * speed)

    def ready(self):
        return self._timer.is_ready()

    def damage(self, target):
        damage = self.power

        if not target.has(Player) and target.target.empty():
            target.target.set(self.entity)

        critcal = False

        if random.randint(1, 10) == 5:
            damage *= 2
            critcal = True

        target.health.reduce(damage)

        self.io.emit('damage-taken', target.id, damage, critcal)

        if not target.health.is_alive():
            target.delete()
            self.io.emit('death', target.id)

class RangedAttack(Component):
    def initialize(self, power=0):
        self.power = power

class Name(Component):
    def initialize(self, name=None):
        self.name = name or 'Player %d' % self.entity.id

    def serialize(self):
        return self.name

    def set(self, name):
        self.name = name or 'Player %d' % self.entity.id
        self.io.emit('name-change', self.entity.id, name)

class Player(Component):
    def initialize(self, uid=None):
        self.uid = uid
        self.connections = set()

    def serialize(self):
        return {
            'uid': self.uid
        }

class Faction(Component):
    def initialize(self, faction):
        self.faction = faction

    def set(self, faction):
        self.faction = faction

    def serialize(self):
        return self.faction

class Health(Component):
    def initialize(self, maximum=0):
        self.current = maximum
        self.maximum = maximum

    def is_alive(self):
        return self.current > 0

    def reduce(self, amount):
        self.current = max(0, self.current - amount)

    def serialize(self):
        return {
            'current': self.current,
            'maximum': self.maximum,
        }

class Mana(Health):
    def initialize(self, maximum=0):
        self.current = maximum
        self.maximum = maximum

    def serialize(self):
        return {
            'current': self.current,
            'maximum': self.maximum,
        }

class Level(Component):
    def initialize(self, level=0):
        self.level = level

    def serialize(self):
        return self.level

class Experience(Component):
    def initialize(self, need=0):
        self.have = 0
        self.need = need

    def serialize(self):
        return {
            'have': self.have,
            'need': self.need,
        }

class Target(Component):
    def initialize(self, target=None):
        self.target = target

    def set(self, target):
        if isinstance(target, int):
            target = self.entity.world.entities[target]

        self.target = target

        world = self.entity.world
        world.io.emit('target', self.entity.id, target.id if target else None)

    def empty(self):
        return self.target is None

    def serialize(self):
        return self.target.id if self.target else None