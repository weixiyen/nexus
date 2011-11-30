import itertools
import yaml
import importlib
import os
from .entity import Entity
from . import logger

ARCHETYPES = 'config/archetypes.yaml'

class EntityManager(object):
    def __init__(self, world, archetypes=None):
        self.world = world
        self._id = itertools.count(1)
        self._entities = {}

        if os.path.exists(ARCHETYPES):
            from tornado import autoreload
            autoreload.watch(ARCHETYPES)

            with open(ARCHETYPES) as f:
                self._archetypes = {}

                for name, archetype in yaml.load(f.read()).items():
                    components = {}

                    for component, kwargs in archetype.items():
                        pieces = component.split('.')
                        module = importlib.import_module('.'.join(pieces[:-1]))

                        try:
                            components[getattr(module, pieces[-1])] = kwargs
                        except Exception:
                            logger.error('Unknown component "%s"' % component)
                            exit(0)

                    self._archetypes[name] = components

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
        entity = Entity(self, archetype=archetype)

        if archetype:
            with entity.assemble():
                items = self._archetypes[archetype].items()

                while items:
                    component, kwargs = items.pop(0)

                    try:
                        if kwargs:
                            entity.install(component, **kwargs)
                        else:
                            entity.install(component)
                    except Exception as e:
                        if len(items) > 0:
                            items.append((component, kwargs))
                        else:
                            logger.error([component, kwargs])
                            raise e

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