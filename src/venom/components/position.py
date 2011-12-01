import venom

class Position(venom.Component):
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

            if self.entity.has(venom.components.Collision):
                self.entity.collision.update()

    def serialize(self):
        return {
            'x': self.x,
            'y': self.y,
        }