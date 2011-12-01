import re

class Component(object):
    @classmethod
    def name(cls):
        s1 = re.sub(r'(.)([A-Z][a-z]+)', r'\1_\2', cls.__name__)
        return re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

    def __init__(self, entity):
        self.entity = entity
        self.world = entity.world
        self.io = self.world.io

    def __repr__(self):
        return '<Component: %s>' % self.__class__.__name__

    def initialize(self, *args, **kwargs):
        pass

    def serialize(self):
        return None

