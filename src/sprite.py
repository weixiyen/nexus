import Image
import os

SPRITE_PATH = os.path.join(os.path.dirname(__file__), '../public/img')

class Sprite(object):
    def __init__(self, src, width=None, height=None, frames=1):
        self.src = os.path.join('sprite', src)
        self.frames = frames
        self.width = width
        self.height = height

        if width is None or height is None:
            image = Image.open(os.path.join(SPRITE_PATH, self.src))

            width, height = image.size

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