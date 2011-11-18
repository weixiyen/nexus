from datetime import datetime, timedelta
import random

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

        self.target = None

        self._last_attack = datetime.now()
        self.game.add_entity(self)

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<%s: %s#%d [%d,%d]>' % (self.__class__.__name__, self.name, self.id, self.x, self.y)

    def serialize(self):
        return {
            'kind': self.__class__.__name__,
            'id': self.id,
            'name': self.name,
            'x': self.x,
            'y': self.y,
            'hp': self.hp,
            'target': self.target.id if self.target else None
        }

    def emit(self, *args):
        self.game.emit(*args)

    def is_attacking(self):
        return self.target is not None

    def attack(self, target=None):
        now = datetime.now()

        target = target or self.target

        if isinstance(self, MovableEntity) and self.game.map.get_distance(self, target) > 1:
            self.find_path_to(target)
        elif self._last_attack <= now - timedelta(seconds=1):
            if target and target.take_damage(1):
                self.game.logger.debug('Attacking %r -> %r' % (self, target))

                if not target.is_alive():
                    self.target = None

            self._last_attack = now

    def nearby(self, radius=3):
        for entity in self.game.entities:
            if entity == self:
                continue

            if self.game.map.get_distance(self, entity) <= radius:
                yield entity

    def is_alive(self):
        return self.hp > 0

    def take_damage(self, damage):
        if self.is_alive():
            if random.randint(1, 10) == 5:
                damage *= 2
                self.game.logger.debug('Critical!')

            self.hp -= damage

            if isinstance(self, Player):
                self.emit('hp', self.hp)

            if not self.is_alive():
                self.game.remove_entity(self)
                self.game.logger.debug('Killed %r' % self)
                self.emit('dead', self.serialize())

                if isinstance(self, Monster):
                    self.game.spawn(self.name)

            return True
        return False

    def iteration(self):
        if self.is_attacking():
            self.attack()
            raise StopIteration

class MovableEntity(Entity):
    def __init__(self, *args, **kwargs):
        Entity.__init__(self, *args, **kwargs)

        self.movement_speed = 500

        self._movement_queue = []
        self._last_movement = datetime.now()

    def move(self, x, y):
        self.x = x
        self.y = y
        self.emit('move', self.serialize())

    def move_to(self, entity):
        self.move(entity.x, entity.y)

    def find_path(self, x, y):
        self._movement_queue = self.game.map.find_route([self.x, self.y], [x, y])

    def find_path_to(self, entity):
        self.find_path(entity.x, entity.y)

    def iteration(self):
        now = datetime.now()

        if self._movement_queue and self._last_movement <= now - timedelta(milliseconds=1000 / self.movement_speed):
            if self.is_attacking() and self.game.map.get_distance(self, self.target) > 1:
                self.find_path_to(self.target)

            dx, dy = self.game.map.get_delta(self._movement_queue.pop(0))

            self.move(self.x + dx, self.y + dy)

            self._last_movement = now

            raise StopIteration

        Entity.iteration(self)

class Player(MovableEntity):
    def __init__(self, *args, **kwargs):
        MovableEntity.__init__(self, *args, **kwargs)

        self.hp = 500
        self.movement_speed = 1000

class Monster(MovableEntity):
    def __init__(self, *args, **kwargs):
        MovableEntity.__init__(self, *args, **kwargs)

        self.hp = 25

        self._patrol_radius = 5
        self._last_patrol = datetime.now()

    def aggro(self):
        if self.is_attacking():
            return

        try:
            self.target = self.nearby().next()
            self.find_path_to(self.target)
            self.game.logger.debug('Targeting %r' % self.target)
        except StopIteration:
            pass

    def iteration(self):
        now = datetime.now()

        try:
            MovableEntity.iteration(self)
        except StopIteration as e:
            self.aggro()
            raise e

        if self._last_patrol <= now - timedelta(seconds=2):
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

            self.find_path(x, y)

            self._last_patrol = now

            self.game.logger.debug('Moving %r' % self)