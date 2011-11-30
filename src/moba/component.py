from venom2.component import Component

class Name(Component):
    def initialize(self, name=None):
        self.set(name)

    def serialize(self):
        return self.name

    def set(self, name):
        self.name = name or 'Player %d' % self.entity.id

class User(Component):
    def initialize(self, uid=None):
        self.id = uid
        self.connections = set()

    def serialize(self):
        return {
            'id': self.id
        }

class Faction(Component):
    def initialize(self, faction):
        self.faction = faction

    def set(self, faction):
        self.faction = faction

    def serialize(self):
        return self.faction

class Health(Component):
    def initialize(self, maximum=0):
        self.current = maximum
        self.maximum = maximum

    def serialize(self):
        return {
            'current': self.current,
            'maximum': self.maximum,
        }

class Mana(Health):
    def initialize(self, maximum=0):
        self.current = maximum
        self.maximum = maximum

    def serialize(self):
        return {
            'current': self.current,
            'maximum': self.maximum,
        }

class Level(Component):
    def initialize(self, level=0):
        self.level = level

    def serialize(self):
        return self.level

class Experience(Component):
    def initialize(self, need=0):
        self.have = 0
        self.need = need

    def serialize(self):
        return {
            'have': self.have,
            'need': self.need,
        }

class Target(Component):
    def initialize(self, target=None):
        self.target = target

    def set(self, target):
        self.target = target

    def serialize(self):
        return self.target.id if self.target else None