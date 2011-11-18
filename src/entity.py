import math
import random
from datetime import datetime, timedelta

class Entity(object):
    id = 0

    def __init__(self, game, name, x=0, y=0):
        Entity.id += 1

        self.id = Entity.id
        self.game = game
        self.name = name
        self.x = x
        self.y = y

        self.hp = 0
        self._target = None

        self._last_attack = datetime.now()
        self.game.add_entity(self)

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<%s: %s#%d [%d,%d]>' % (self.__class__.__name__, self.name, self.id, self.x, self.y)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'x': self.x,
            'y': self.y,
            'hp': self.hp,
            'target': self._target.id if self._target else None
        }

    def emit(self, *args):
        self.game.emit(*args)

    def is_attacking(self):
        return self._target is not None

    def attack(self, target=None):
        now = datetime.now()

        if self._last_attack <= now - timedelta(milliseconds=100):
            target = target or self._target

            if target and target.take_damage(1):
                self.game.logger.debug('Attacking %r -> %r' % (self, self._target))

                if not target.is_alive():
                    self._target = None

            self._last_attack = now

    def get_distance(self, x, y):
        xd = x - self.x
        yd = y - self.y
        return math.sqrt(xd * xd + yd * yd)

    def nearby(self, radius=3):
        for entity in self.game.entities:
            if entity == self:
                continue

            if entity.get_distance(self.x, self.y) <= radius:
                yield entity

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, damage):
        if self.is_alive():
            if random.randint(1, 10) == 5:
                damage *= 2
                self.game.logger.debug('Critical!')

            self.hp -= damage

            if not self.is_alive():
                self.game.remove_entity(self)
                self.game.logger.debug('Killed %r' % self)
                self.emit('dead', self.serialize())
                self.game.spawn(self.name)

            return True
        return False

    def iteration(self):
        if self.is_attacking():
            self.attack()
            return False
        return True

class MovableEntity(Entity):
    def move(self, x, y):
        self.x = x
        self.y = y
        self.emit('move', self.serialize())

    def move_to(self, entity):
        self.move(entity.x, entity.y)

class Player(MovableEntity):
    pass

class Monster(MovableEntity):
    def __init__(self, *args, **kwargs):
        MovableEntity.__init__(self, *args, **kwargs)

        self._home_x = self.x
        self._home_y = self.y
        self._patrol_radius = 5
        self._walk_queue = []

        self._last_move = datetime.now()
        self.hp = 25

    def aggro(self):
        if self.is_attacking():
            return

        try:
            self._target = self.nearby().next()
            self.find_route(self._target.x, self._target.y)
            self.game.logger.debug('Targeting %r' % self._target)
        except StopIteration:
            pass

    def find_route(self, x, y):
        self._walk_queue = self.game.map.find_route([self.x, self.y], [x, y])

    def iteration(self):
        now = datetime.now()

        if self._walk_queue:
            if self.is_attacking():
                  if self.get_distance(self._target.x, self._target.y) > 1:
                      self.find_route(self._target.x, self._target.y)

            op = self._walk_queue.pop(0)

            self.x += self.game.map.DX[op]
            self.y += self.game.map.DY[op]

            self.move_to(self)

            self.aggro()

            return

        if MovableEntity.iteration(self):
            if self._last_move <= now - timedelta(seconds=2):
                x = self.x
                y = self.y

                if random.randint(0, 1):
                    x += random.randint(-self._patrol_radius, self._patrol_radius)
                else:
                    y += random.randint(-self._patrol_radius, self._patrol_radius)

                if x < 0:
                    x = self.game.map.width - 1
                elif x > self.game.map.width - 1:
                    x = 0

                if y < 0:
                    y = self.game.map.height - 1
                elif y > self.game.map.height - 1:
                    y = 0

                self.find_route(x, y)

                self._last_move = now

                self.game.logger.debug('Moving %r' % self)
            else:
                self.aggro()