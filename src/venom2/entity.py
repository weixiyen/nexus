from contextlib import contextmanager

class Entity(object):
    __slots__ = ['id', 'world', '_components', '_assembling']

    def __init__(self, manager):
        self.id = manager.next_id()
        self.world = manager.world
        self._components = {}
        self._assembling = False

    def __repr__(self):
        return '<%s: %d>' % (self.__class__.__name__, self.id)

    def __getitem__(self, item):
        return self._components[item]

    def __getattr__(self, item):
        try:
            return self._components[item]
        except KeyError:
            return object.__getattribute__(self, item)

    def serialize(self):
        return {
            'id': self.id,
            'components': {name: component.serialize() for name, component in self._components.items()}
        }

    @property
    def exists(self):
        """True if the entity still exists in the world"""
        return self in self.world.entities

    @contextmanager
    def assemble(self):
        self._assembling = True
        yield self
        self._assembling = False
        # inform systems

    def _component_name(self, component):
        return component if isinstance(component, basestring) else component.name()

    def install(self, component, *args, **kwargs):
        assert self._assembling
        self._components[self._component_name(component)] = component(self, *args, **kwargs)

    def uninstall(self, component):
        assert self._assembling
        del self._components[self._component_name(component)]

    def has(self, component):
        return self._component_name(component) in self._components

    def delete(self):
        """Delete the entity from its world. This removes all of its
        component data. If then entity has already been deleted,
        this call does nothing.
        """
        self.world.entities.discard(self)