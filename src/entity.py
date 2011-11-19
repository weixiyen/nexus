from datetime import datetime, timedelta
import random

class Delayer(object):
    def __init__(self, ms=100):
        self.delta = timedelta(milliseconds=ms)
        self.last_time = None

    def is_ready(self):
        now = datetime.now()

        if self.last_time is None or self.last_time <= now - self.delta:
            self.last_time = now
            return True

        return False

BASE_STATS = {
    'hp': 0,
    'mp': 0,
    'attack': 0,
    'range_attack': 0,
    'movement_speed': 500,
    'aggro_range': 3,
    'leash': 15,
    'patrol': 10
}

class Entity(object):
    id = 0

    def __init__(self, game, name, x=0, y=0):
        Entity.id += 1

        self.id = Entity.id
        self.game = game

        self.name = name
        self.x = x
        self.y = y
        self.target = None

        self.base_stats = BASE_STATS.copy()
        self.stats = self.base_stats.copy()

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
            'stats': self.stats,
            'target': self.target.id if self.target else None
        }

    def emit(self, *args):
        self.game.emit(*args)

    def is_attacking(self):
        return self.target is not None

    def set_target(self, target):
        self.target = target

        if target is None:
            self.emit('target', self.id, None)
        else:
            self.emit('target', self.id, target.id)

    def attack(self, target=None):
        if not self.stats['attack']:
            return

        target = target or self.target

        if not target.is_alive():
            self.set_target(None)
            return

        if self.game.iteration_counter % 10:
            if self.game.map.get_distance(self, target) > self.stats['leash']:
                self.set_target(None)
                self._movement_queue = None
                self.game.logger.debug('Lost Aggro %r -> %r' % (self, target))
            return

        now = datetime.now()

        if isinstance(self, MovableEntity) and self.game.map.get_distance(self, target) > 1:
            self.move_to(target)
            self._execute_movement_queue(True)
        elif self._last_attack <= now - timedelta(seconds=1):
            if target and target.take_damage(self, self.stats['attack']):
                self.game.logger.debug('Attacking %r -> %r' % (self, target))

                if not target.is_alive():
                    self.set_target(None)

            self._last_attack = now

    def nearby(self, radius=3):
        for entity in self.game.entities:
            if entity == self:
                continue

            if isinstance(entity, self.__class__):
                continue

            if self.game.map.get_distance(self, entity) <= radius:
                yield entity

    def is_alive(self):
        return self.stats['hp'] > 0

    def take_damage(self, from_, damage):
        if self.is_alive():
            if not isinstance(self, Player) and self.target is None:
                self.set_target(from_)

            if random.randint(1, 10) == 5:
                damage *= 2
                self.game.logger.debug('Critical!')

            self.stats['hp'] -= damage

            if isinstance(self, Player):
                self.emit('hp', self.stats['hp'])

            if not self.is_alive():
                self.game.remove_entity(self)
                self.game.logger.debug('Killed %r' % self)
                self.emit('death', self.id)

#                if isinstance(self, Monster):
#                    self.game.spawn(self.name)

            return True
        return False

    def next_iteration(self):
        if self.is_attacking():
            self.attack()
            raise StopIteration

class MovableEntity(Entity):
    def __init__(self, *args, **kwargs):
        Entity.__init__(self, *args, **kwargs)

        self._movement_queue = []
        self._delayer = Delayer(self.stats['movement_speed'])

    def _move(self, x, y):
        self.x = x
        self.y = y
        self.emit('move', self.id, x, y)

    def _move_to(self, entity):
        self._move(entity.x, entity.y)

    def move(self, x, y):
        self._movement_queue = self.game.map.find_path([self.x, self.y], [x, y])

    def move_to(self, entity):
        self.move(entity.x, entity.y)

    def next_move(self):
        return self._movement_queue.pop()

    def is_moving(self):
        return len(self._movement_queue) != 0

    def _execute_movement_queue(self, ignore_atk=False):
        if self.is_moving() and self._delayer.is_ready():
            if not ignore_atk and self.is_attacking() and self.game.map.get_distance(self, self.target) > 2:
                self.move_to(self.target)

            x, y = self.next_move()

            self._move(x, y)

            raise StopIteration

    def next_iteration(self):
        self._execute_movement_queue()
        Entity.next_iteration(self)

class Player(MovableEntity):
    def __init__(self, *args, **kwargs):
        self.uid = kwargs.pop('uid')
        self.connections = set()

        MovableEntity.__init__(self, *args, **kwargs)

        self.stats['hp'] = 500

class Monster(MovableEntity):
    def __init__(self, *args, **kwargs):
        MovableEntity.__init__(self, *args, **kwargs)

        self.stats['hp'] = 10
        self.stats['attack'] = 1
        self.stats['movement_speed'] = 80

        self._last_patrol = datetime.now()

    def aggro(self):
        if self.is_attacking():
            return

        try:
            self.set_target(self.nearby(self.stats['aggro_range']).next())
            self.move_to(self.target)
            self.game.logger.debug('Targeting %r' % self.target)
        except StopIteration:
            pass

    def next_iteration(self):
        now = datetime.now()

        try:
            MovableEntity.next_iteration(self)
        except StopIteration as e:
            raise e
        finally:
            self.aggro()

        if not self.is_moving() and self._last_patrol <= now - timedelta(seconds=random.randint(5, 10)):
            x = self.x
            y = self.y

            if random.randint(0, 1):
                x += random.randint(-self.stats['patrol'], self.stats['patrol'])
            else:
                y += random.randint(-self.stats['patrol'], self.stats['patrol'])

            if x < 0:
                x = self.game.map.width - 1
            elif x > self.game.map.width - 1:
                x = 0

            if y < 0:
                y = self.game.map.height - 1
            elif y > self.game.map.height - 1:
                y = 0

            self.move(x, y)

            self._last_patrol = now

            self.game.logger.debug('Moving %r' % self)

class Turret(Entity):
    def __init__(self, *args, **kwargs):
        Entity.__init__(self, *args, **kwargs)

        self.stats['hp'] = 100
        self.stats['attack'] = 10

    def aggro(self):
        if self.is_attacking():
            return

        try:
            self.set_target(self.nearby(self.stats['aggro_range']).next())
            self.game.logger.debug('Targeting %r' % self.target)
        except StopIteration:
            self.set_target(None)

    def next_iteration(self):
        self.aggro()
        Entity.next_iteration(self)
