import math
import logging
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
        target = target or self._target

        if target and target.take_damage(1):
            logging.debug('Attacking %r -> %r' % (self, self._target))
            self.emit('log', 'Attacking %r -> %r' % (self, self._target))

            if not target.is_alive():
                self._target = None

    def get_distance(self, x, y):
        return math.sqrt(self.x * x + self.y * y)

    def nearby(self, radius=10):
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
                logging.debug('Critical!')
                self.emit('log', 'Critical!')

            self.hp -= damage

            if not self.is_alive():
                self.game.remove_entity(self)
                logging.debug('Killed %r' % self)
                self.emit('log', 'Killed %r' % self)
                self.emit('dead', self.serialize())

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
        logging.debug('Moving %r' % self)
        self.emit('log', 'Moving %r' % self)
        self.emit('move', self.serialize())

    def move_to(self, entity):
        self.move(entity.x, entity.y)

class Player(MovableEntity):
    pass

class Monster(MovableEntity):
    IDLE = 0

    def __init__(self, *args, **kwargs):
        MovableEntity.__init__(self, *args, **kwargs)

        self._home_x = self.x
        self._home_y = self.y
        self._patrol_radius = 5

        self._last_move = datetime.now()
        self.hp = 10

    def iteration(self):
        now = datetime.now()

        if MovableEntity.iteration(self):
            if self._last_move <= now - timedelta(seconds=1):
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

                self.move(x, y)

                self._last_move = now
            else:
                try:
                    self._target = self.nearby().next()
                    self.move_to(self._target)
                    logging.debug('Targeting %r' % self._target)
                    self.emit('log', 'Targeting %r' % self._target)
                except StopIteration:
                    pass