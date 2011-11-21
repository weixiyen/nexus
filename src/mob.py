from entity import Entity, MonsterEntity, StationaryMonsterEntity, PlayerEntity
from limiter import Limiter

class Minion(MonsterEntity):
    pass

class Turret(StationaryMonsterEntity):
    pass

class Nexus(Entity):
    def __init__(self, *args, **kwargs):
        Entity.__init__(self, *args, **kwargs)

        self._tick_limiter = Limiter(1000)

    def next_iteration(self):
        if self._tick_limiter.is_ready():
            for entity in self.get_nearby_entities(20):
                if isinstance(entity, PlayerEntity):
                    entity.heal(5)
                else:
                    entity.damage_taken(None, 1)
