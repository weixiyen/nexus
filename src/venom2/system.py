import abc
from .component import Movement

class System(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, manager):
        self.world = manager.world

    def process_one(self, entity):
        self.process([entity])

    @abc.abstractmethod
    def process(self, entities):
        pass

class MovementSystem(System):
    def process(self, entities):
        for entity in entities:
            if not entity.has(Movement):
                continue

            movement = entity.movement

            if movement.ready():
                position = entity.position
                position.x, position.y = movement.queue.pop()
                self.world.io.emit('move', entity.id, position.x, position.y)