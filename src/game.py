from map import Map
from entity import MovableEntity
import random
import logging

class Game(object):
    def __init__(self):
        self.map = Map(50, 50)
        self._entities = {}

    def spawn(self, name, x=None, y=None):
        if x is None or y is None:
            while True:
                x = random.randint(0, self.map.width - 1)
                y = random.randint(0, self.map.height - 1)

                if not self.map.is_obstacle(x, y):
                    break

        mob = MovableEntity(self, name, x, y)

        logging.debug('Spawning %r' % mob)

    @property
    def entities(self):
        return self._entities.values()

    def add_entity(self, entity):
        self._entities[entity.id] = entity

    def remove_entity(self, entity):
        del self._entities[entity.id]
