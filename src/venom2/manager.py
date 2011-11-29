import itertools
from .entity import Entity

class EntityManager(object):
    def __init__(self, world):
        self.world = world
        self._id = itertools.count(1)
        self._entities = {}

    def __getitem__(self, key):
        return self._entities.get(key)

    def __delitem__(self, key):
        return self.remove(key)

    def __iter__(self):
        for entity in self._entities.values():
            yield entity

    def next_id(self):
        return self._id.next()

    def create(self, archetype=None):
        entity = Entity(self)
        self._entities[entity.id] = entity
        return entity

    def remove(self, key):
        del self._entities[key]

    def discard(self, key):
        try:
            self.remove(key)
        except KeyError:
            pass

class SystemManager(object):
    def __init__(self, world):
        self.world = world
        self._systems = []

    def __iter__(self):
        return self._systems.__iter__()

    def install(self, system):
        self._systems.append(system(self))