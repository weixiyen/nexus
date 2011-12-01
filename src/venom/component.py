import re
import Image
import os
import random
import timer

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

class Position(Component):
    def initialize(self):
        self.x = None
        self.y = None
        self.home = None

    def set(self, x, y):
        first_position = self.x is None

        self.x = x
        self.y = y

        if first_position:
            self.home = (x, y)

            if self.entity.has(Collision):
                self.entity.collision.update()

    def serialize(self):
        return {
            'x': self.x,
            'y': self.y,
        }

class Movement(Component):
    def initialize(self, speed=1):
        self._map = self.entity.world.map
        self._timer = timer.Timer(speed * 100.0)

        self.speed = speed
        self.queue = None

    def busy(self):
        return not not self.queue

    def ready(self):
        return self.queue and self._timer.is_ready()

    def stop(self):
        self.queue = None

    def move(self, x, y, offset=None):
        position = self.entity.position

        self.queue = self._map.find_path((position.x, position.y), (x, y))

        if offset:
            self.queue = self.queue[offset:]

    def serialize(self):
        return {
            'speed': self.speed
        }

class Collision(Component):
    def update(self):
        position = self.entity.position
        sprite = self.entity.sprite
        self.entity.world.map.add_collision(position.x, position.y, sprite.width, sprite.height / 1.8)

class Sprite(Component):
    PATH = os.path.join(os.path.dirname(__file__), '../../public/img')

    _cache = {}

    def initialize(self, src=None, width=None, height=None, **animate):
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