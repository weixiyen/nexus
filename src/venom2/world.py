import datetime
import tornado.ioloop

from . import manager, io
from .map import Map

class World(object):
    def __init__(self, width, height):
        self.step_rate = 60
        self.map = Map(width, height)
        self.systems = manager.SystemManager(self)
        self.entities = manager.EntityManager(self)
        self.io = io.Network(self)

        self._ioloop =  tornado.ioloop.IOLoop.instance()
        self._step_rate = datetime.timedelta(milliseconds=1000.0 / self.step_rate)

    def set_io_flush_callback(self, callback):
        self._io_flush_callback = callback

    def serialize(self):
        return {
            'map': self.map.serialize(),
            'entities': [entity.serialize() for entity in self.entities]
        }

    def step(self):
        for system in self.systems:
            system.process(self.entities)

        self.io.flush(self._io_flush_callback)

        self._ioloop.add_timeout(self._step_rate, self.step)

    def activate(self):
        self.step()

    def deactivate(self):
        pass