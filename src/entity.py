from operator import itemgetter
import random
from timer import Timer
from map import Map
import ability
from sprite import Sprite

LEVEL = {}

for level in range(1, 20):
    LEVEL[level] = 100 * level

MAX_LEVEL = max(LEVEL.keys())

class Entity(object):
    id = 0

    def __init__(self, instance, name, x=0, y=0, sprite=None, faction=None, **stats):
        Entity.id += 1

        self.id = Entity.id
        self.instance = instance

        self.name = name
        self.faction = faction
        self.x = x
        self.y = y
        self._home = (x, y)
        self.target = None

        if sprite is None and hasattr(self.__class__, 'sprite'):
            sprite = self.__class__.sprite

        self.sprite = sprite if isinstance(sprite, Sprite) else Sprite(sprite)

        self.base_stats = self.get_base_stats()
        self.base_stats.update(stats)

        self.stats = self.base_stats.copy()

        self.movement_speed = self.stats['movement_speed']

        self.set_level(stats.pop('level', 1))

        self.buffs = []

        self._attack_timer = None
        self._mp_regen_timer = Timer(500)

        self.instance.add_entity(self)

    def set_level(self, level=1):
        self.level = level

        self.experience = {
            'have': 0,
            'need': LEVEL[level]
        }

        self.stats['hp'] = self.base_stats['hp'] * level
        self.stats['mp'] = self.base_stats['mp'] * level
        self.stats['attack'] = self.base_stats['attack'] * level

        self.hp = self.stats['hp']
        self.mp = self.stats['mp']

    def get_base_stats(self):
        return {
            'hp': 0,
            'mp': 0,
            'attack': 0,
            'attack_speed': 5,
            'movement_speed': 4,
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
            'sprite': self.sprite.serialize(),
            'x': self.x,
            'y': self.y,
            'hp': self.hp,
            'mp': self.mp,
            'faction': self.faction,
            'level': self.level,
            'experience': self.experience,
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

        if target == self:
            return

        if target and target.faction == self.faction:
            return

        self.target = target

        if self.is_alive():
            self.emit('target', self.id, target.id if target else None)

    def apply_buff(self, buff_type, source=None, duration=5000):
        for buff in self.buffs:
            if isinstance(buff, buff_type):
                return

        buff = buff_type(self, source, duration)

        if buff.applied:
            self.buffs.append(buff)

    def attack(self):
        if not self.stats['attack']:
            return

        target = self.target

        if self._attack_timer is None:
            self._attack_timer = Timer(self.stats['attack_speed'] * 100)

        if not target.is_alive():
            self.set_target(None)
        elif self.instance.iteration_counter % 5 and not isinstance(self, PlayerEntity):
            if self.instance.map.get_distance(self, target) > self.stats['aggro_radius'] * 8:
                self.set_target(None)

                if isinstance(self, MovableEntity):
                    self.stop_movement()

                self.instance.logger.debug('Lost Aggro %r -> %r' % (self, target))
        elif isinstance(self, MovableEntity) and self.instance.map.get_distance(self, target) > 1:
            self.move_to(target)
            self._execute_movement_queue(True)
        elif self._attack_timer.is_ready():
            self._execute_attack(target)

            if not target.is_alive():
                self.set_target(None)

    def _execute_attack(self, target):
        if target.damage_taken(self, self.stats['attack']):
            self.instance.logger.debug('Attacking %r -> %r' % (self, target))

    def get_nearby_entities(self, radius):
        entities = []

        for entity in self.instance.entities:
            if entity == self:
                continue

            if not entity.is_alive():
                continue

            if isinstance(entity, ParticleEntity):
                continue

            distance = self.instance.map.get_distance(self, entity)

            if distance <= radius:
                entities.append((distance, entity))

        entities.sort(key=itemgetter(0))

        for _, entity in entities:
            yield entity

    def get_nearby_enemies(self, radius):
        for entity in self.get_nearby_entities(radius):
            if entity.faction != self.faction:
                yield entity

    def get_nearby_allies(self, radius):
        for entity in self.get_nearby_entities(radius):
            if entity.faction == self.faction:
                yield entity

    def get_entities_at(self, coordinates, radius):
        for entity in self.instance.entities:
            if entity == self:
                continue

            if not entity.is_alive():
                continue

            if isinstance(entity, ParticleEntity):
                continue

            if self.instance.map.get_distance(coordinates, entity) <= radius:
                yield entity

    def get_enemies_at(self, coordinates, radius):
        for entity in self.get_entities_at(coordinates, radius):
            if entity.faction != self.faction:
                yield entity

    def is_alive(self):
        return self.hp > 0 or isinstance(self, ParticleEntity)

    def damage_taken(self, from_, damage):
        if self.is_alive():
            if not isinstance(self, PlayerEntity) and self.target is None and from_:
                self.set_target(from_)

            critcal = False

            if random.randint(1, 10) == 5:
                damage *= 2
                self.instance.logger.debug('Critical!')
                critcal = True

            self.hp -= damage

            self.emit('damage-taken', self.id, damage, critcal, from_.faction if from_ else None)

            if not self.is_alive():
                if isinstance(self, MovableEntity):
                    self.stop_movement()

                if not self.stats['respawn']:
                    self.instance.remove_entity(self)
                else:
                    self.set_target(None)

                if from_ and isinstance(from_, PlayerEntity):
                    from_.increase_experience(self.level * 50)

                self.instance.logger.debug('Killed %r' % self)
                self.emit('death', self.id)

            return True

        return False

    def increase_experience(self, amt):
        self.experience['have'] += amt

        overflow = self.experience['have'] - self.experience['need']

        if overflow >= 0:
            if self.level < MAX_LEVEL:
                self.level_up(overflow)
        else:
            self.emit('experience', self.id, amt)

    def level_up(self, have=0):
        self.set_level(self.level + 1)
        self.experience['have'] = have

        self.emit('level-up', self.id, {
            'stats': self.stats,
            'hp': self.hp,
            'mp': self.mp,
            'experience': self.experience,
            'level': self.level
        })

        # incase we earned more then we need
        self.increase_experience(0)

    def use_mp(self, amt):
        if self.mp >= amt:
            self.mp -= amt
            self.emit('mp', self.id, -amt)
            return True

        return False

    def heal(self, amt):
        hp = self.hp + amt

        if hp > self.stats['hp']:
            hp = self.stats['hp']

            amt = hp - self.hp

            if amt > 0:
                self.emit('heal', self.id, amt)
        else:
            self.emit('heal', self.id, amt)

        self.hp = hp

    def next_iteration(self):
        if not self.is_alive():
            if self.instance.iteration_counter % 1000 == 0 and self.stats['respawn']:
                self.respawn()
            raise StopIteration

        if self.buffs:
            self.buffs = [buff for buff in self.buffs if not buff.elapsed]

        if self.mp < self.stats['mp'] and self._mp_regen_timer.is_ready():
            self.mp += 5
            self.emit('mp', self.id, 5)

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
        self._movement_queue = self.instance.map.find_path([self.x, self.y], [x, y], not isinstance(self, ParticleEntity))

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

        if hasattr(self, '_movement_timer'):
            self.emit('set-movement-speed', self.id, movement_speed)

        self._movement_timer = Timer(movement_speed * 100)

    def _execute_movement_queue(self, ignore_atk=False):
        if self.is_moving() and self._movement_timer.is_ready():
            if not ignore_atk and self.is_attacking() and self.instance.map.get_distance(self, self.target) > 2:
                self.move_to(self.target)

            try:
                self._move(*self._next_move())
            except IndexError:
                pass

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

    def ability(self, action, target_id, coordinates):
        target = self.instance.get_entity(target_id)

        if action == 1 and self.use_mp(10): # aoe
            ability.aoe(self, coordinates)
        elif action == 2 and self.use_mp(5): # slow
            ability.slow(target)
        elif action == 3 and self.use_mp(15): # haste myself
            ability.haste(self)
        elif action == 4 and self.use_mp(5): # poison
            ability.poison(self, target)
        elif action == 5 and self.use_mp(50): # ultimate
            ability.ultimate(self)

    def get_base_stats(self):
        base_stats = MovableEntity.get_base_stats(self)
        base_stats.update({
            'hp': 100,
            'mp': 100,
            'movement_speed': 2,
            'attack': 5,
        })
        return base_stats

class MonsterEntity(MovableEntity):
    def __init__(self, *args, **kwargs):
        MovableEntity.__init__(self, *args, **kwargs)

        self._patrol_timer = Timer(10000, True)

    def aggro(self):
        if self.is_attacking():
            return

        try:
            self.set_target(self.get_nearby_enemies(self.stats['aggro_radius']).next())
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

        if not self.is_moving() and self._patrol_timer.is_ready():
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
            self.set_target(self.get_nearby_enemies(self.stats['aggro_radius']).next())
            self.instance.logger.debug('Targeting %r' % self.target)
        except StopIteration:
            if self.target:
                self.set_target(None)

    def next_iteration(self):
        self.aggro()
        Entity.next_iteration(self)

    def get_base_stats(self):
        base_stats = Entity.get_base_stats(self)
        base_stats.update({
            'aggro_radius': 20,
            'attack_speed': 25,
        })
        return base_stats

class ParticleEntity(MovableEntity):
    def __init__(self, *args, **kwargs):
        self.parent = kwargs.pop('parent')
        self._target_coords = None
        MovableEntity.__init__(self, *args, **kwargs)

    def suicide(self):
        self.instance.remove_entity(self)
        self.emit('death', self.id)

    def attack(self):
        target = self.target

        if not target.is_alive():
            self.suicide()
        elif self.instance.map.get_distance(self, target) > 0:
            target_coords = (target.x, target.y)

            if self._target_coords != target_coords:
                self._target_coords = target_coords

                self.move_to(target)

                if not self.is_moving():
                    self.suicide()
                else:
                    self._execute_movement_queue(True)
        else:
            target.damage_taken(self.parent, self.parent.stats['attack'])
            self.suicide()

    def get_base_stats(self):
        base_stats = MovableEntity.get_base_stats(self)
        base_stats.update({
            'movement_speed': 1,
        })
        return base_stats