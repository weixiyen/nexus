import random
from limiter import Limiter
from map import Map
import buffs

class Entity(object):
    id = 0

    def __init__(self, instance, name, x=0, y=0, **stats):
        Entity.id += 1

        self.id = Entity.id
        self.instance = instance

        self.name = name
        self.x = x
        self.y = y
        self._home = (x, y)
        self.target = None

        self.stats = self.get_base_stats()
        self.stats.update(stats)

        self.hp = self.stats['hp']
        self.movement_speed = self.stats['movement_speed']

        self.buffs = []

        self._attack_limiter = None

        self.instance.add_entity(self)

    def get_base_stats(self):
        return {
            'hp': 0,
            'attack': 0,
            'attack_speed': 5,
            'movement_speed': 5,
            'aggro_radius': 3,
            'patrol_radius': 8,
            'respawn': True
        }

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
            'movement_speed': self.movement_speed,
            'stats': self.stats,
            'target': self.target.id if self.target else None
        }

    def emit(self, *args):
        self.instance.emit(*args)

    def respawn(self):
        self.x, self.y = self._home
        self.hp = self.stats['hp']
        self.movement_speed = self.stats['movement_speed']
        self.emit('spawn', self.serialize())

    def is_attacking(self):
        return self.target is not None

    def set_target(self, target):
        if isinstance(target, int):
            target = self.instance.get_entity(target)

        self.target = target

        if self.is_alive():
            self.emit('target', self.id, target.id if target else None)

    def apply_buff(self, buff_type, duration=5000):
        buff = buff_type(self, duration)

        if buff.applied:
            self.buffs.append(buff)

    def attack(self):
        if not self.stats['attack']:
            return

        target = self.target

        if self._attack_limiter is None:
            self._attack_limiter = Limiter(self.stats['attack_speed'] * 100)

        if not target.is_alive():
            self.set_target(None)
        elif self.instance.iteration_counter % 5 and not isinstance(self, PlayerEntity):
            if self.instance.map.get_distance(self, target) > self.stats['aggro_radius'] * 4:
                self.set_target(None)

                if isinstance(self, MovableEntity):
                    self.stop_movement()

                self.instance.logger.debug('Lost Aggro %r -> %r' % (self, target))
        else:
            if isinstance(self, MovableEntity) and self.instance.map.get_distance(self, target) > 1:
                self.move_to(target)
                self._execute_movement_queue(True)
            elif self._attack_limiter.is_ready():
                if target and target.damage_taken(self, self.stats['attack']):
                    self.instance.logger.debug('Attacking %r -> %r' % (self, target))

                    if not target.is_alive():
                        self.set_target(None)

    def get_nearby_entities(self, radius):
        for entity in self.instance.entities:
            if entity == self:
                continue

            if isinstance(entity, self.__class__):
                continue

            if not entity.is_alive():
                continue

            if self.instance.map.get_distance(self, entity) <= radius:
                yield entity

    def is_alive(self):
        return self.hp > 0

    def damage_taken(self, from_, damage):
        if self.is_alive():
            if not isinstance(self, PlayerEntity) and self.target is None:
                self.set_target(from_)

            critcal = False

            if random.randint(1, 10) == 5:
                damage *= 2
                self.instance.logger.debug('Critical!')
                critcal = True

            self.hp -= damage

            self.emit('damage-taken', self.id, damage, critcal)

            if not self.is_alive():
                if isinstance(self, MovableEntity):
                    self.stop_movement()

                self.set_target(None)

                self.instance.logger.debug('Killed %r' % self)
                self.emit('death', self.id)

            return True

        return False

    def next_iteration(self):
        if not self.is_alive():
            if self.instance.iteration_counter % 1000 == 0 and self.stats['respawn']:
                self.respawn()
            raise StopIteration

        if self.buffs:
            self.buffs = [buff for buff in self.buffs if not (buff.elapsed and buff.complete())]

        if self.is_attacking():
            self.attack()
            raise StopIteration

class MovableEntity(Entity):
    def __init__(self, *args, **kwargs):
        Entity.__init__(self, *args, **kwargs)

        self._movement_queue = []
        self.set_movement_speed(self.stats['movement_speed'])

    def _move(self, x, y):
        self.x = x
        self.y = y
        self.emit('move', self.id, x, y)

    def _move_to(self, entity):
        self._move(entity.x, entity.y)

    def move(self, x, y):
        self._movement_queue = self.instance.map.find_path([self.x, self.y], [x, y])

    def move_to(self, entity):
        self.move(entity.x, entity.y)

    def _next_move(self):
        return self._movement_queue.pop()

    def is_moving(self):
        return len(self._movement_queue) != 0

    def stop_movement(self):
        self._movement_queue = []

    def set_movement_speed(self, movement_speed):
        self.movement_speed = movement_speed

        if hasattr(self, '_movement_limiter'):
            self.emit('set-movement-speed', self.id, movement_speed)

        self._movement_limiter = Limiter(movement_speed * 100)

    def _execute_movement_queue(self, ignore_atk=False):
        if self.is_moving() and self._movement_limiter.is_ready():
            if not ignore_atk and self.is_attacking() and self.instance.map.get_distance(self, self.target) > 2:
                self.move_to(self.target)

            x, y = self._next_move()

            self._move(x, y)

            raise StopIteration

    def next_iteration(self):
        self._execute_movement_queue()
        Entity.next_iteration(self)

class PlayerEntity(MovableEntity):
    def __init__(self, *args, **kwargs):
        self.uid = kwargs.pop('uid')
        self.connections = set()

        MovableEntity.__init__(self, *args, **kwargs)

        if not self.name:
            self.name = 'Player %d' % self.id

    def set_name(self, name):
        if name == self.name:
            return

        if not name:
            name = 'Player %d' % self.id

        self.name = name

        self.emit('name-change', self.id, name)

    def ability(self, ability, target_id, coordinates):
        entities = []

        for entity in self.instance.entities:
             if entity == self:
                 continue

             if isinstance(entity, self.__class__):
                 continue

             if not entity.is_alive():
                 continue

             if self.instance.map.get_distance(coordinates, entity) <= 5:
                 entities.append(entity)

        if entities:
            damage = 10 / len(entities)

            for entity in entities:
                entity.apply_buff(buffs.Slow)
                entity.damage_taken(self, damage)

    def get_base_stats(self):
        base_stats = MovableEntity.get_base_stats(self)
        base_stats.update({
            'hp': 100,
            'movement_speed': 2,
            'attack': 5,
        })
        return base_stats

class MonsterEntity(MovableEntity):
    def __init__(self, *args, **kwargs):
        MovableEntity.__init__(self, *args, **kwargs)

        self._patrol_limiter = Limiter(2000, True)

    def aggro(self):
        if self.is_attacking():
            return

        try:
            self.set_target(self.get_nearby_entities(self.stats['aggro_radius']).next())
            self.move_to(self.target)
            self.instance.logger.debug('Targeting %r' % self.target)
        except StopIteration:
            pass

    def next_iteration(self):
        try:
            MovableEntity.next_iteration(self)
        except StopIteration as e:
            raise e
        finally:
            self.aggro()

        if not self.is_moving() and self._patrol_limiter.is_ready():
            if Map.get_distance((self.x, self.y), self._home) > self.stats['patrol_radius']:
                x, y = self._home
            else:
                x = self.x
                y = self.y

                if random.randint(0, 1):
                    x += random.randint(-self.stats['patrol_radius'], self.stats['patrol_radius'])
                else:
                    y += random.randint(-self.stats['patrol_radius'], self.stats['patrol_radius'])

                if x < 0:
                    x = self.instance.map.width - 1
                elif x > self.instance.map.width - 1:
                    x = 0

                if y < 0:
                    y = self.instance.map.height - 1
                elif y > self.instance.map.height - 1:
                    y = 0

            self.move(x, y)

            self.instance.logger.debug('Moving %r' % self)

class StationaryMonsterEntity(Entity):
    def aggro(self):
        if self.is_attacking():
            return

        try:
            self.set_target(self.get_nearby_entities(self.stats['aggro_radius']).next())
            self.instance.logger.debug('Targeting %r' % self.target)
        except StopIteration:
            self.set_target(None)

    def next_iteration(self):
        self.aggro()
        Entity.next_iteration(self)

    def get_base_stats(self):
        base_stats = Entity.get_base_stats(self)
        base_stats.update({
            'aggro_radius': 20
        })
        return base_stats