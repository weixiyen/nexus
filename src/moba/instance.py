import venom
from components import Player, Faction
from systems import PatrolSystem, AggroSystem, FollowSystem, CombatSystem, ProjectileSystem, ManaRegenSystem, SpawnSystem

_instance = None

class Instance(object):
    def __init__(self, width, height):
        self.characters = set()

        self.world = venom.World(width, height)
        self.world.set_io_flush_callback(self._io_flush)
        self.world.step()

        for archetype in ['Tree', 'Rock']:
            for i in xrange(25):
                self.spawn(archetype)

        for i in xrange(50):
            self.spawn('Minion')

        # Team Blue
        self.spawn('Nexus', (14, 117), 0)
        self.spawn('Turret', (28, 97), 0)
        self.spawn('Turret', (34, 112), 0)
        self.spawn('Turret', (28, 127), 0)
        self.spawn('Turret', (62, 57), 0)
        self.spawn('Turret', (62, 112), 0)
        self.spawn('Turret', (62, 168), 0)

        # Team Pink
        self.spawn('NexusPink', (174, 117), 1)
        self.spawn('TurretPink', (160, 97), 1)
        self.spawn('TurretPink', (154, 112), 1)
        self.spawn('TurretPink', (160, 127), 1)
        self.spawn('TurretPink', (124, 62), 1)
        self.spawn('TurretPink', (124, 121), 1)
        self.spawn('TurretPink', (124, 168), 1)

        self.world.systems.install(venom.systems.MovementSystem)
        self.world.systems.install(PatrolSystem)
        self.world.systems.install(CombatSystem)
        self.world.systems.install(AggroSystem, 10)
        self.world.systems.install(FollowSystem)
        self.world.systems.install(ProjectileSystem)
        self.world.systems.install(ManaRegenSystem)
        self.world.systems.install(SpawnSystem, 500)

    def spawn(self, archetype, position=None, faction=None):
        entity = self.world.entities.create(archetype)

        if faction is not None:
            with entity.assemble():
                entity.install(Faction, faction)

        if position is None:
            position = self.world.map.get_random_position()

        x, y = position

        entity.position.set(x, y)

    def _io_flush(self, instructions):
        for character in self.characters:
            for connection in character.player.connections:
                connection.emit('instructions', instructions)

    @staticmethod
    def get():
        global _instance

        if _instance is None:
            _instance = Instance(188, 219)

        return _instance

    def serialize(self):
        return self.world.serialize()

    def add_player(self, conn, name):
        for character in self.characters:
            if character.player.uid == conn.uid:
                character.name.set(self._player_name(character, name))
                character.player.connections.add(conn)
                return character.player

        if len(self.characters) % 2:
            x, y = (20, 117)
            faction = 0
        else:
            x, y = (168, 107)
            faction = 1

        character = self.world.entities.create('Character')

        with character.assemble():
            character.install(Player, conn.uid)
            character.install(Faction, faction)

        character.name.set(self._player_name(character, name))
        character.position.set(x, y)
        character.player.connections.add(conn)

        self.characters.add(character)

        return character.player

    def _player_name(self, entity, name):
        return name or 'Player %d' % entity.id

    def remove_player(self, conn):
        player = conn.player

        player.connections.remove(conn)

        if not player.connections:
            character = player.entity
            self.characters.remove(character)
            character.delete()
