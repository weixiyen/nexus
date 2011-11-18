from map import Map
import entity
import random
import logging
import tornado.ioloop
import datetime

class Game(object):
    def __init__(self):
        self.participants = set()

        self.map = Map(50, 50)
        self._entities = {}

        self.iteration()

        self.logger = logging.getLogger('game')
        self.logger.setLevel(logging.DEBUG)

    def serialize(self):
        return {
            'map': self.map.serialize(),
            'entities': [entity.serialize() for entity in self.entities]
        }

    def add_participant(self, p):
        self.participants.add(p)

    def remove_participant(self, p):
        self.participants.remove(p)

    def emit(self, event, *args):
        for p in self.participants:
            p.emit(event, *args)

    def iteration(self):
        for entity in self.entities:
            entity.iteration()

        tornado.ioloop.IOLoop.instance().add_timeout(datetime.timedelta(milliseconds=30), self.iteration)

    def spawn(self, name, x=None, y=None, type_=entity.Monster):
        if x is None or y is None:
            while True:
                x = random.randint(0, self.map.width - 1)
                y = random.randint(0, self.map.height - 1)

                if not self.map.is_obstacle(x, y):
                    break

        mob = type_(self, name, x, y)

        self.logger.debug('Spawning %r' % mob)

    @property
    def entities(self):
        return self._entities.values()

    def add_entity(self, entity):
        self._entities[entity.id] = entity

    def remove_entity(self, entity):
        del self._entities[entity.id]
