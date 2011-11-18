import math

class Entity(object):
    def __init__(self, game, name, x=0, y=0):
        self.game = game
        self.name = name
        self.x = x
        self.y = y

        self.game.add_entity(self)

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<%s: (%d) %s [%d,%d]>' % (self.__class__.__name__, self.id, self.name, self.x, self.y)

    @property
    def id(self):
        return id(self)

    def get_distance(self, x, y):
        return math.sqrt(self.x * x + self.y * y)

    def nearby(self, radius=10):
        for entity in self.game.entities:
            if entity.get_distance(self.x, self.y) <= radius:
                yield entity

class MovableEntity(Entity):
    def move(self, x, y):
        self.x = x
        self.y = y

class PlayableEntity(MovableEntity):
    pass