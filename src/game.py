from map import Map
import entity
import random
import logging
import tornado.ioloop

class Game(object):
    def __init__(self):
        self.participants = set()

        self.map = Map(50, 50)
        self._entities = {}

        self.iteration_counter = 0

        tornado.ioloop.PeriodicCallback(self.next_iteration, 30).start()

        self.logger = logging.getLogger('game')
#        self.logger.setLevel(logging.DEBUG)

    def serialize(self):
        return {
            'map': self.map.serialize(),
            'entities': [entity.serialize() for entity in self.entities]
        }

    def add_participant(self, p):
        self.participants.add(p)

        for e in self.entities:
            if isinstance(e, entity.Player):
                if e.uid == p.uid:
                    e.connections.add(p)
                    return e

        e = self.spawn(p.uid, uid=p.uid, type_=entity.Player)
        e.connections.add(p)
        return e

    def remove_participant(self, p):
        self.participants.remove(p)

        p.entity.connections.remove(p)

        if not p.entity.connections:
            self.remove_entity(p.entity)

    def emit(self, event, *args):
        for p in self.participants:
            p.emit(event, *args)

    def next_iteration(self):
        self.iteration_counter += 1

        for entity in self.entities:
            try:
                entity.next_iteration()
            except StopIteration:
                pass

    def spawn(self, name, x=None, y=None, type_=entity.Monster, **kwargs):
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