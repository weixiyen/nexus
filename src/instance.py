from map import Map
from entity import Player, Monster, Turret
import random
import logging
import tornado.ioloop
from datetime import timedelta

FPS = 60

_instances = {}

class Instance(object):
    def __init__(self, id):
        self.id = id
        self.ioloop =  tornado.ioloop.IOLoop.instance()
        self.deadline = timedelta(milliseconds=1000 / FPS)
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
                instance.spawn('Lizard')

#            instance.spawn('Turret', type_=Turret)
#            instance.spawn('Turret', type_=Turret)
#            instance.spawn('Turret', type_=Turret)
#            instance.spawn('Turret', type_=Turret)

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

    def add_player(self, conn):
        for e in self.entities:
            if isinstance(e, Player):
                if e.uid == conn.uid:
                    e.connections.add(conn)
                    return e

        player = self.spawn(conn.uid, uid=conn.uid, type_=Player)
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
            self.ioloop.add_timeout(self.deadline, self.next_iteration)
        else:
            self.stop()

    def spawn(self, name, x=None, y=None, type_=Monster, **kwargs):
        if x is None or y is None:
            while True:
                x = random.randint(0, self.map.width - 1)
                y = random.randint(0, self.map.height - 1)

                if self.map.is_walkable(x, y):
                    break

        mob = type_(self, name, x, y, **kwargs)

        self.logger.debug('Spawning %r' % mob)

        return mob

    @property
    def entities(self):
        return self._entities.values()

    def add_entity(self, entity):
        self._entities[entity.id] = entity
        self.emit('spawn', entity.serialize())

    def remove_entity(self, entity):
        try:
            del self._entities[entity.id]
        except KeyError:
            pass