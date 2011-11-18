from map import Map
import entity
import random
import logging
import tornado.ioloop
import datetime

class Game(object):
    def __init__(self):
        self.map = Map(20, 20)
        self._entities = {}

        self.iteration()

    def iteration(self):
        for entity in self.entities:
            entity.iteration()

        tornado.ioloop.IOLoop.instance().add_timeout(datetime.timedelta(milliseconds=30), self.iteration)


        logging.debug('Entities Alive: %r' % self.entities)

    def spawn(self, name, x=None, y=None, type_=entity.Monster):
        if x is None or y is None:
            while True:
                x = random.randint(0, self.map.width - 1)
                y = random.randint(0, self.map.height - 1)

                if not self.map.is_obstacle(x, y):
                    break

        mob = type_(self, name, x, y)

        logging.debug('Spawning %r' % mob)

    @property
    def entities(self):
        return self._entities.values()

    def add_entity(self, entity):
        self._entities[entity.id] = entity

    def remove_entity(self, entity):
        del self._entities[entity.id]
