import math
import logging
import random
from datetime import datetime, timedelta

class Entity(object):
    def __init__(self, game, name, x=0, y=0):
        self.game = game
        self.name = name
        self.x = x
        self.y = y
        self.hp = 0

        self.game.add_entity(self)

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<%s: (%d) %s [%d,%d]>' % (self.__class__.__name__, self.id, self.name, self.x, self.y)

    @property
    def id(self):
        return id(self)

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
            self.hp -= damage

            if not self.is_alive():
                self.game.remove_entity(self)
                logging.debug('Killed %r' % self)

            return True
        return False

    def iteration(self):
        pass

class MovableEntity(Entity):
    def move(self, x, y):
        self.x = x
        self.y = y
        logging.debug('Moving %r' % self)

    def move_to(self, entity):
        self.move(entity.x, entity.y)

class Player(MovableEntity):
    pass

class Monster(MovableEntity):
    IDLE = 0


    def __init__(self, *args, **kwargs):
        MovableEntity.__init__(self, *args, **kwargs)

        self._target = None
        self._last_move = datetime.now()
        self.hp = 10

    def is_attacking(self):
        return self._target is not None

    def attack(self, target=None):
        target = target or self._target

        if target and target.take_damage(1):
            logging.debug('Attacking %r -> %r' % (self, self._target))

            if not target.is_alive():
                self._target = None

    def iteration(self):
        now = datetime.now()

        if self.is_attacking():
            self.attack()
        elif self._last_move <= now - timedelta(seconds=1):
            x = self.x
            y = self.y

            if random.randint(0, 1):
                x += random.randint(1, 10)
            else:
                y += random.randint(1, 10)

            if x >= 50:
                x = 0

            if y >= 50:
                y = 0

            self.move(x, y)

            self._last_move = now
        else:
            try:
                self._target = self.nearby().next()
                self.move_to(self._target)
                logging.debug('Targeting %r' % self._target)
            except StopIteration:
                pass