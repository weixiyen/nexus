import Image
import os
import random
import venom

class Sprite(venom.Component):
    PATH = os.path.join(os.path.dirname(__file__), '../../../public/img')

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