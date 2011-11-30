from moba.component import Patrol, Aggro, Target, Health, Kind, Attack, Player, Projectile
from venom2.system import System
from venom2.component import Movement

class ProjectileSystem(System):
    def process(self, entities):
        for entity in entities.filter(Projectile):
            suicide = not entity.target.target.health.is_alive()

            if not suicide and not entity.movement.busy():
                entity.projectile.parent.attack.damage(entity.target.target)
                suicide = True

            if suicide:
                entity.delete()
                self.io.emit('death', entity.id)

class CombatSystem(System):
    def process(self, entities):
        for entity in entities.filter(Attack):
            if entity.target.empty() or not entity.attack.ready():
                continue

            target = entity.target.target

            if target.health.is_alive():
                if entity.has(Movement):
                    self.attack(entity, target)
                else:
                    self.projectile(entity, target)
            else:
                entity.target.set(None)

    def projectile(self, entity, target):
        projectile = self.world.entities.create('Projectile')
        projectile.position.set(entity.position.x, entity.position.y)
        projectile.target.set(target)
        projectile.projectile.parent = entity
        self.io.emit('spawn', projectile.serialize())

    def attack(self, entity, target):
        if self.world.map.distance((entity.position.x, entity.position.y), (target.position.x, target.position.y)) > 1:
            return

        entity.attack.damage(target)

class PatrolSystem(System):
    def process(self, entities):
        for entity in entities.filter(Patrol):
            movement = entity.movement
            patrol = entity.patrol

            if not movement.busy() and patrol.ready():
                movement.move(*patrol.next())

class FollowSystem(System):
    def process(self, entities):
        for entity in entities.filter(Target, Movement):
            if entity.target.empty():
                continue

            target = entity.target.target

            start = entity.position.x, entity.position.y
            end = target.position.x, target.position.y

            distance = self.world.map.distance(start, end)

            if entity.has(Aggro) and distance > entity.aggro.radius * 8:
                entity.target.set(None)
                entity.movement.stop()
            elif distance > 1:
                x, y = end
                entity.movement.move(x, y, 1)

class AggroSystem(System):
    def process(self, entities):
        for entity in entities.filter(Aggro):
            target = entity.target

            if target.empty() or not entity.has(Movement):
                try:
                    target.set(self.get_nearby_enemies(entity, entity.aggro.radius).next())
                except StopIteration:
                    pass

    def get_nearby_enemies(self, entity, radius):
        for enemy in self.world.entities.at(entity.position.x, entity.position.y, radius):
            if enemy == entity or \
               not enemy.has(Health) or \
               not enemy.health.is_alive() or \
               (enemy.has(Kind) and entity.has(Kind) and enemy.kind == entity.kind):
                continue

            yield enemy