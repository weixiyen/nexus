import venom2
from venom2.component import Position, Sprite, Movement
from venom2.system import MovementSystem
from component import *

_instance = None

class Instance(object):
    def __init__(self, width, height):
        self.players = set()

        self.world = venom2.World(width, height)
        self.world.set_io_flush_callback(self._io_flush)
        self.world.step()

        for archetype in ['Tree', 'Rock']:
            for i in xrange(25):
                tree = self.world.entities.create(archetype)
                tree.position.set(*self.world.map.get_random_position())

        self.world.systems.install(MovementSystem)

    def _io_flush(self, instructions):
        for player in self.players:
            for connection in player.user.connections:
                connection.emit('instructions', instructions)

    @staticmethod
    def get():
        global _instance

        if _instance is None:
            _instance = Instance(188, 219)

        return _instance

    def serialize(self):
        serialized = self.world.serialize()
        serialized['props'] = {}
        return serialized

    def add_player(self, conn, name):
        for player in self.players:
            if player.user.id == conn.uid:
                player.name.set(name)
                player.user.connections.add(conn)
                return player

        if len(self.players) % 2:
            x, y = (20, 117)
            faction = 0
        else:
            x, y = (168, 107)
            faction = 1

        player = self.world.entities.create('Player')

        with player.assemble():
            player.install(User, conn.uid)
            player.install(Faction, faction)

        player.name.set(name)
        player.position.set(x, y)
        player.user.connections.add(conn)

        self.players.add(player)

        return player

    def remove_player(self, conn):
        player = conn.player

        player.user.connections.remove(conn)

        if not player.user.connections:
            self.players.remove(player)
            player.delete()
