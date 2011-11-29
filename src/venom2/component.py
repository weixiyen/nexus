import abc
import re
import Image
import os
import random
import timer

class Component(object):
    __metaclass__ = abc.ABCMeta

    @classmethod
    def name(cls):
        s1 = re.sub(r'(.)([A-Z][a-z]+)', r'\1_\2', cls.__name__)
        return re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

    def __init__(self, entity, *args, **kwargs):
        self.entity = entity
        self.initialize(*args, **kwargs)

    def __repr__(self):
        return '<Component: %s>' % self.__class__.__name__

    def initialize(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def serialize(self):
        pass

class Position(Component):
    def initialize(self, x, y):
        self.x = x
        self.y = y

    def serialize(self):
        return {
            'x': self.x,
            'y': self.y,
        }

class Movement(Component):
    def initialize(self, speed=1):
        self._map = self.entity.world.map

        self.speed = speed
        self.queue = None

    def ready(self):
        return self.queue and self.timer.is_ready()

    def go(self, x, y):
        position = self.entity.position
        self.timer = timer.Timer(self.speed * 100.0)
        self.queue = self._map.find_path((position.x, position.y), (x, y))

    def serialize(self):
        return {
            'speed': self.speed
        }

class Collision(Component):
    def initialize(self):
        position = self.entity['position']
        sprite = self.entity['sprite']
        self.entity.world.map.add_collision(position.x, position.y, sprite.width, sprite.height / 1.8)

class Sprite(Component):
    PATH = os.path.join(os.path.dirname(__file__), '../../public/img')

    _cache = {}

    def initialize(self, src, width=None, height=None, **animate):
        if isinstance(src, (list, tuple)):
            src = random.choice(src)

        self.src = os.path.join('sprite', src)
        self.width = width
        self.height = height

        self.animate = {
            'walk': 0,
            'stand': 0
        }
        self.animate.update(animate)

        if width is None or height is None:
            if self.src not in Sprite._cache:
                image = Image.open(os.path.join(Sprite.PATH, self.src))
                width, height = Sprite._cache[self.src] = image.size
            else:
                width, height = Sprite._cache[self.src]

            if self.width is None:
                self.width = width

                if self.animate['walk']:
                    self.width /= self.animate['walk'] + self.animate['stand']

            if self.height is None:
                directions = 1

                if self.animate['walk'] or self.animate['stand']:
                    directions = 8

                self.height = height / directions

    def serialize(self):
        return {
            'src': self.src,
            'width': self.width,
            'height': self.height,
            'animate': self.animate,
        }