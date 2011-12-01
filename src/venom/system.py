import abc

class System(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, manager):
        self.world = manager.world
        self.io = manager.world.io

    def process_one(self, entity):
        self.process([entity])

    @abc.abstractmethod
    def process(self, entities):
        pass