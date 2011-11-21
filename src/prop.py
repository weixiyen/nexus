class Prop(object):
    id = 0

    def __init__(self, instance, x=0, y=0):
        Prop.id += 1

        self.id = Prop.id
        self.instance = instance

        self.x = x
        self.y = y

        self.instance.add_prop(self)

    def __str__(self):
        return self.__class__.__name__

    def __repr__(self):
        return '<%s: #%d [%d,%d]>' % (self.__class__.__name__, self.id, self.x, self.y)

    def serialize(self):
        return {
            'kind': self.__class__.__name__,
            'id': self.id,
            'x': self.x,
            'y': self.y
        }

class Tree1(Prop):
    pass

class Tree2(Prop):
    pass

class Tree3(Prop):
    pass

class Tree4(Prop):
    pass