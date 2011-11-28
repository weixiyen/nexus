from contextlib import contextmanager

class Entity(object):
    """
    Concept!

    entity = Entity(world) OR entity = world.entity()

    with entity.assemble:
        entity.install(Name)
        entity.install(Movement)
        entity.install(Position)
        entity.install(Target)
        entity.install(Patrol)
        entity.install(Aggro)

    """

    __slots__ = ['world', '_id', '_components']

    def __init__(self, world):
        self.world = world
        self._id = world.nextId()
        self._components = {}

    @property
    def id(self):
        return self._id

    @property
    def exists(self):
        """True if the entity still exists in the world"""
        return self in self.world.entities

    @contextmanager
    def assemble(self):
        # lock
        yield
        # unlock
        # inform systems

    def install(self, component, *args, **kwargs):
        self._components[component] = component(*args, **kwargs)

    def uninstall(self, component):
        del self._components[component]

    def delete(self):
        """Delete the entity from its world. This removes all of its
        component data. If then entity has already been deleted,
        this call does nothing.
        """
        self.world.entities.discard(self)