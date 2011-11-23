import Image
import os
import random

SPRITE_PATH = os.path.join(os.path.dirname(__file__), '../public/img')
CACHE = {}

class Sprite(object):
    def __init__(self, src, width=None, height=None, frames=1):
        if isinstance(src, (list, tuple)):
            src = random.choice(src)

        self.src = os.path.join('sprite', src)
        self.frames = frames
        self.width = width
        self.height = height

        if width is None or height is None:
            if self.src not in CACHE:
                image = Image.open(os.path.join(SPRITE_PATH, self.src))
                width, height = CACHE[self.src] = image.size
            else:
                width, height = CACHE[self.src]

            if self.width is None:
                self.width = width / frames

            if self.height is None:
                self.height = height

    def serialize(self):
        return {
            'src': self.src,
            'width': self.width,
            'height': self.height,
        }