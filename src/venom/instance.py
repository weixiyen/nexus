import tornado.ioloop
import datetime
import simplejson

from venom.map import Map
from venom.entity import Entity, PlayerEntity
from venom.sprite import Sprite
from venom import prop
import venom

FPS = 60

class Instance(object):
    id = 0

    def __init__(self, width, height):
        self.id = Instance.id = Instance.id + 1

        self._ioloop =  tornado.ioloop.IOLoop.instance()
        self._delay = datetime.timedelta(milliseconds=1000.0 / FPS)

        self.running = False

        self.players = set()
        self.map = Map(width, height)

        self._entities = {}
        self._props = {}

        self._emit_buffer = []

        self.iteration_counter = 0

    def start(self):
        if not self.running:
            self.running = True
            venom.logger.debug('Starting %r' % self)
            self.next_iteration()

    def stop(self):
        self.running = False
        venom.logger.debug('Stopping  %r' % self)

    def serialize(self):
        return {
            'map': self.map.serialize(),
            'entities': [entity.serialize() for entity in self.entities if entity.is_alive()],
            'props': [prop.serialize() for prop in self.props]
        }

    def add_player(self, conn, name, **kwargs):
        for e in self.entities:
            if isinstance(e, PlayerEntity):
                if e.uid == conn.uid:
                    e.set_name(name)
                    e.connections.add(conn)
                    return e

        if len(self.players) % 2:
            x, y = (20, 117)
            faction = 'blue'
        else:
            x, y = (168, 107)
            faction = 'pink'

        player = self.spawn(name, x, y, uid=conn.uid, faction=faction, kind=PlayerEntity, sprite=Sprite('character/cray.png', walk=6, stand=1), **kwargs)
        player.connections.add(conn)

        self.players.add(player)

        self.start() # start if not running...

        return player

    def remove_player(self, conn):
        conn.player.connections.remove(conn)

        if not conn.player.connections:
            self.players.remove(conn.player)
            self.remove_entity(conn.player)

    def emit(self, event, *args):
        self._emit_buffer.append((event, args))

    def flush(self):
        if self._emit_buffer:
            buffer = simplejson.dumps(self._emit_buffer)

            for player in self.players:
                for conn in player.connections:
                    conn.emit('instructions', buffer)

            self._emit_buffer = []

    def next_iteration(self):
        self.iteration_counter += 1

        for entity in self.entities:
            try:
                entity.next_iteration()
            except StopIteration:
                pass

        self.flush()

        if self.players:
            self._ioloop.add_timeout(self._delay, self.next_iteration)
        else:
            self.stop()

    def spawn(self, name, x=None, y=None, kind=Entity, **kwargs):
        if x is None or y is None:
            x, y = self.map.get_random_position()

        mob = kind(self, name, x, y, **kwargs)

        venom.logger.debug('Spawning %r' % mob)

        return mob

    @property
    def entities(self):
        return self._entities.values()

    def get_entity(self, entity_id):
        return self._entities.get(entity_id)

    def add_entity(self, entity):
        self.emit('spawn', entity.serialize())
        self._entities[entity.id] = entity

    def remove_entity(self, entity):
        try:
            del self._entities[entity.id]
        except KeyError:
            pass

    def place(self, x=None, y=None, kind=prop.Prop, **kwargs):
        if x is None or y is None:
            x, y = self.map.get_random_position()

        prop_ = kind(self, x=x, y=y, **kwargs)

        venom.logger.debug('Placing %r' % prop_)

        return prop_

    @property
    def props(self):
        return self._props.values()

    def get_prop(self, prop_id):
        return self._props.get(prop_id)

    def add_prop(self, prop):
        self.emit('place', prop.serialize())
        self._props[prop.id] = prop

    def remove_prop(self, prop):
        del self._props[prop.id]