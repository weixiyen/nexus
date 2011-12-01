import itertools
import yaml
import importlib
import os
import collections
from .entity import Entity
from . import logger
import venom

ARCHETYPES = 'config/archetypes.yaml'

class EntityManager(object):
    def __init__(self, world):

        self.world = world
        self._id = itertools.count(1)
        self._entities = {}
        self._components = collections.defaultdict(set)

        if os.path.exists(ARCHETYPES):
            from tornado import autoreload
            autoreload.watch(ARCHETYPES)

            with open(ARCHETYPES) as f:
                self._archetypes = {}

                archetypes = yaml.load(f.read())

                for name in venom.utils.topsort({name: archetype.get('extend') for name, archetype in archetypes.items()}):
                    archetype = archetypes[name]

                    components = {}

                    if 'extend' in archetype:
                        components = self._archetypes[archetype['extend']].copy()

                    if 'components' in archetype:
                        for component, kwargs in archetype['components'].items():
                            pieces = component.split('.')
                            module = importlib.import_module('.'.join(pieces[:-1]))

                            try:
                                cls = getattr(module, pieces[-1])

                                if cls not in components:
                                    components[cls] = kwargs
                                else:
                                    components[cls] = components[cls].copy()
                                    components[cls].update(kwargs)
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

    def filter(self, *components):
        entities = None

        for component in components:
            if entities is None:
                entities = self._components[component].copy()
            elif entities:
                if component.startswith('-'):
                    entities -= self._components[component[1:]]
                else:
                    entities &= self._components[component]
            else:
                break

        return entities

    def at(self, x, y, radius=1):
        entities = []

        for entity in self.filter('position'):
            position = entity.position
            distance = self.world.map.distance((x, y), (position.x, position.y))

            if distance <= radius:
                entities.append((distance, entity))

        entities.sort()

        for _, entity in entities:
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

#    def reindex(self, entity, components):
#        for entities in self._components.values():
#            try:
#                entities.remove(entity)
#            except KeyError:
#                pass
#
#        for component in components:
#            self._components[component].add(entity)

    def remove(self, key):
        if not isinstance(key, int):
            key = key.id

        del self._entities[key]

    def discard(self, key):
        try:
            self.remove(key)

            for component in key._components.keys():
                self._components[component].remove(key)
        except KeyError:
            pass

class SystemManager(object):
    def __init__(self, world):
        self.world = world
        self._systems = []

    def __iter__(self):
        for mod, system in self._systems:
            if not self.world.iteration % mod:
                yield system

    def install(self, system, mod=1):
        self._systems.append((mod, system(self)))