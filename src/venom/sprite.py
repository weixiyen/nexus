import Image
import os
import random

SPRITE_PATH = os.path.join(os.path.dirname(__file__), '../../public/img')
CACHE = {}

class Sprite(object):
    def __init__(self, src, width=None, height=None, **animate):
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
            if self.src not in CACHE:
                image = Image.open(os.path.join(SPRITE_PATH, self.src))
                width, height = CACHE[self.src] = image.size
            else:
                width, height = CACHE[self.src]

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