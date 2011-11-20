import random
import logging
import tornado.ioloop
import datetime

from map import Map
from entity import Entity, PlayerEntity
import monsters

FPS = 60

_instances = {}

class Instance(object):
    def __init__(self, id):
        self.id = id

        self._ioloop =  tornado.ioloop.IOLoop.instance()
        self._delay = datetime.timedelta(milliseconds=1000 / FPS)
        self.running = False

        self.players = set()

        self.map = Map(50, 50)
        self._entities = {}

        self.iteration_counter = 0

        self.logger = logging.getLogger('instance:%d' % self.id)
        self.logger.setLevel(logging.DEBUG)

    @classmethod
    def get(cls, instance_id):
        global _instances

        instance_id = int(instance_id or 1)

        try:
            return _instances[instance_id]
        except KeyError:
            instance = Instance(instance_id)
            _instances[instance_id] = instance

            for i in xrange(25):
                instance.spawn('Lizard',  kind=monsters.Lizard, hp=10, attack=1)

            instance.spawn('Turret', kind=monsters.Turret, hp=100, attack=3)

            instance.start()

            return instance

    def start(self):
        if not self.running:
            self.running = True
            self.logger.debug('Starting')
            self.next_iteration()

    def stop(self):
        self.running = False
        self.logger.debug('Stopping')

    def serialize(self):
        return {
            'map': self.map.serialize(),
            'entities': [entity.serialize() for entity in self.entities]
        }

    def add_player(self, conn, name, **kwargs):
        for e in self.entities:
            if isinstance(e, PlayerEntity):
                if e.uid == conn.uid:
                    e.set_name(name)
                    e.connections.add(conn)
                    return e

        player = self.spawn(name, uid=conn.uid, kind=PlayerEntity, **kwargs)
        player.connections.add(conn)

        self.players.add(player)

        self.start() # start if not running...

        return player

    def remove_player(self, conn):
        conn.player.connections.remove(conn)

        if not conn.player.connections:
            self.players.remove(conn.player)
            self.remove_entity(conn.player)

    def emit(self, event, *args):
        for player in self.players:
            for conn in player.connections:
                conn.emit(event, *args)

    def next_iteration(self):
        self.iteration_counter += 1

        for entity in self.entities:
            try:
                entity.next_iteration()
            except StopIteration:
                pass

        if self.players:
            self._ioloop.add_timeout(self._delay, self.next_iteration)
        else:
            self.stop()

    def spawn(self, name, x=None, y=None, kind=Entity, **kwargs):
        if x is None or y is None:
            while True:
                x = random.randint(0, self.map.width - 1)
                y = random.randint(0, self.map.height - 1)

                if self.map.is_walkable(x, y):
                    break

        mob = kind(self, name, x, y, **kwargs)

        self.logger.debug('Spawning %r' % mob)

        return mob

    @property
    def entities(self):
        return self._entities.values()

    def get_entity(self, entity_id):
        return self._entities.get(entity_id)

    def add_entity(self, entity):
        self.emit('spawn', entity.serialize())
        self._entities[entity.id] = entity

    def remove_entity(self, entity):
        try:
            del self._entities[entity.id]
        except KeyError:
            pass