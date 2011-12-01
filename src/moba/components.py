import venom
import random

class Death(venom.Component):
    def serialize(self):
        return True

class Respawn(venom.Component):
    pass

class Family(venom.Component):
    def initialize(self, family=None):
        self.family = family or self.entity._archetype

    def __eq__(self, other):
        return self.family == other.family

class Faction(venom.Component):
    def initialize(self, faction=None):
        self.faction = faction

    def __eq__(self, other):

        if self.faction is None:
            return False

        return self.faction == other.faction

    def set(self, faction):
        self.faction = faction

    def serialize(self):
        return self.faction

class Aggro(venom.Component):
    def initialize(self, radius=0):
        self.radius = radius

class Projectile(venom.Component):
    def initialize(self):
        self.parent = None

class Patrol(venom.Component):
    def initialize(self, radius=0, rate=10):
        self.radius = radius
        self._timer = venom.utils.Timer(1000.0 * rate)

    def ready(self):
        return self._timer.is_ready()

    def next(self):
        if not hasattr(self, '_points'):
            entity = self.entity
            world = entity.world
            position = entity.position
            self._points = world.map.get_points_in_radius(position.x, position.y, self.radius)

        return random.choice(self._points)

class Attack(venom.Component):
    def initialize(self, power=0, speed=5, projectile=None):
        self.power = power
        self.speed = speed
        self.projectile = projectile
        self._timer = venom.utils.Timer(100.0 * speed)

    def ready(self):
        return self._timer.is_ready()

    def damage(self, target):
        damage = self.power

        if not target.has('player') and target.target.empty():
            target.target.set(self.entity)

        critcal = False

        if random.randint(1, 10) == 5:
            damage *= 2
            critcal = True

        target.health.reduce(damage)

        self.io.emit('damage-taken', target.id, damage, critcal)

        if not target.health.is_alive():
            self.entity.target.set(None)

            if not target.has('respawn'):
                target.delete()
            else:
                target.target.set(None)

                with target.assemble():
                    target.install(Death)

            self.io.emit('death', target.id)

            if self.entity.has('level'):
                self.entity.level.experience(50)

class RangedAttack(venom.Component):
    def initialize(self, power=0):
        self.power = power

class Name(venom.Component):
    def initialize(self, name=''):
        self.name = name

    def serialize(self):
        return self.name

    def set(self, name):
        self.name = name
        self.io.emit('name-change', self.entity.id, name)

class Player(venom.Component):
    def initialize(self, uid=None):
        self.uid = uid
        self.connections = set()

    def serialize(self):
        return {
            'uid': self.uid
        }

class Health(venom.Component):
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
        self._timer = venom.utils.Timer(1000.0)

    def regen(self):
        if self._timer.is_ready():
            if self.current < self.maximum:
                amount = self.maximum * 0.10
                self.current = min(self.current + amount, self.maximum)
                self.io.emit('mp', self.entity.id, amount)

    def reduce(self, amount):
        self.current = max(0, self.current - amount)

    def serialize(self):
        return {
            'current': self.current,
            'maximum': self.maximum,
        }

class Level(venom.Component):
    LEVEL = {}

    for level in range(1, 20):
        LEVEL[level] = 100 * level

    MAX_LEVEL = max(LEVEL.keys())

    def initialize(self, level=1):
        self.set(level)

    def set(self, level):
        self.level = level
        self.have = 0
        self.need = Level.LEVEL[level]

    def experience(self, amt):
        self.have += amt

        overflow = self.have - self.need

        if overflow >= 0:
            if self.level < Level.MAX_LEVEL:
                self.up(overflow)
        else:
            self.io.emit('experience', self.entity.id, amt)

    def up(self, have=0):
        self.set(self.level + 1)
        self.have = have

        self.io.emit('level-up', self.entity.id, self.serialize())

        # in case we earned more then we need
        self.experience(0)

    def serialize(self):
        return {
            'level': self.level,
            'experience': {
                'have': self.have,
                'need': self.need,
            }
        }

class Target(venom.Component):
    def initialize(self, target=None):
        self.target = target

    def set(self, target):
        if isinstance(target, int):
            target = self.entity.world.entities[target]

        if target and self.entity.has('faction') and target.has('faction') and self.entity.faction == target.faction:
            return

        if target == self.entity:
            return

        self.target = target

        self.io.emit('target', self.entity.id, target.id if target else None)

    def empty(self):
        return self.target is None

    def serialize(self):
        return self.target.id if self.target else None