from venom.sprite import Sprite

class Prop(object):
    id = 0

    def __init__(self, instance, sprite=None, x=0, y=0):
        Prop.id += 1

        self.id = Prop.id
        self.instance = instance

        self.x = x
        self.y = y

        if sprite is None and hasattr(self.__class__, 'sprite'):
            sprite = self.__class__.sprite

        self.sprite = sprite if isinstance(sprite, Sprite) else Sprite(sprite)

        self.instance.map.block(x, y, self.sprite.width, self.sprite.height)
        self.instance.add_prop(self)

    def __str__(self):
        return self.__class__.__name__

    def __repr__(self):
        return '<%s: #%d [%d,%d]>' % (self.__class__.__name__, self.id, self.x, self.y)

    def serialize(self):
        return {
            'kind': self.__class__.__name__,
            'id': self.id,
            'sprite': self.sprite.serialize(),
            'x': self.x,
            'y': self.y
        }

class Tree(Prop):
    sprite = [
        'prop/tree1.png',
        'prop/tree2.png',
        'prop/tree3.png',
        'prop/tree4.png',
    ]

class Rock(Prop):
    sprite = [
        'prop/rock1.png',
        'prop/rock2.png',
        'prop/rock3.png',
        'prop/rock4.png',
    ]