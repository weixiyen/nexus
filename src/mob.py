from entity import Entity, MonsterEntity, StationaryMonsterEntity, PlayerEntity
from timer import Timer

class Minion(MonsterEntity):
    pass

class Tower(StationaryMonsterEntity):
    pass

class Nexus(Entity):
    def __init__(self, *args, **kwargs):
        Entity.__init__(self, *args, **kwargs)

        self._tick_timer = Timer(1000)

    def set_target(self, target):
        pass

    def next_iteration(self):
        if self._tick_timer.is_ready():
            for entity in self.get_nearby_entities(20):
                if isinstance(entity, PlayerEntity):
                    entity.heal(5)
                else:
                    entity.damage_taken(self, 5)
