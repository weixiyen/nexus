from sprite import Sprite

class Prop(object):
    id = 0

    def __init__(self, instance, sprite=None, x=0, y=0):
        Prop.id += 1

        self.id = Prop.id
        self.instance = instance

        self.x = x
        self.y = y
        self.sprite = sprite if isinstance(sprite, Sprite) else Sprite(sprite)

        self.instance.map.block(x, y)
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
    pass

class Rock(Prop):
    pass