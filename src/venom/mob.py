from venom.entity import Entity, MonsterEntity, StationaryMonsterEntity, ParticleEntity
from venom.timer import Timer
from venom.sprite import Sprite

class Minion(MonsterEntity):
    sprite = Sprite('character/robot.png', walk=6, stand=1)

class Tower(StationaryMonsterEntity):
    def _execute_attack(self, target):
        particle = self.instance.spawn('%s (Attack)' % self.name,
            x=self.x,
            y=self.y - self.sprite.height / 16 + 1,
            faction=self.faction,
            kind=TowerAttack,
            parent=self,
            respawn=False,
            sprite=Sprite('projectile/bolt-%s.png' % self.faction, walk=3),
        )

        particle.set_target(target)

class TowerAttack(ParticleEntity):
    pass

class Nexus(Entity):
    def __init__(self, *args, **kwargs):
        Entity.__init__(self, *args, **kwargs)

        self._tick_timer = Timer(1000)

    def set_target(self, target):
        pass

    def next_iteration(self):
        if not self.is_alive():
            if self.instance.iteration_counter % 1000 == 0 and self.stats['respawn']:
                self.respawn()
            raise StopIteration

        if self._tick_timer.is_ready():
            for entity in self.get_nearby_enemies(20):
                entity.damage_taken(self, 1)

            for entity in self.get_nearby_allies(20):
                entity.heal(1)