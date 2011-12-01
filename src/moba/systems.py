from moba.components import Death
import venom

class SpawnSystem(venom.System):
    def process(self, entities):
        for entity in entities.filter('death', 'respawn'):
            entity.health.current = entity.health.maximum
            entity.position.set(*entity.position.home)

            with entity.assemble():
                entity.uninstall(Death)

            self.io.emit('spawn', entity.serialize())

class ManaRegenSystem(venom.System):
    def process(self, entities):
        for entity in entities.filter('mana'):
            entity.mana.regen()

class ProjectileSystem(venom.System):
    def process(self, entities):
        for entity in entities.filter('projectile'):
            suicide = not entity.target.target.health.is_alive()

            if not suicide and not entity.movement.busy():
                entity.projectile.parent.attack.damage(entity.target.target)
                suicide = True

            if suicide:
                entity.delete()
                self.io.emit('death', entity.id)

class CombatSystem(venom.System):
    def process(self, entities):
        for entity in entities.filter('attack'):
            if entity.target.empty() or not entity.attack.ready():
                continue

            target = entity.target.target

            if target.health.is_alive():
                if not entity.has('movement') and entity.attack.projectile:
                    self.projectile(entity, target)
                else:
                    self.attack(entity, target)
            else:
                entity.target.set(None)

    def projectile(self, entity, target):
        projectile = self.world.entities.create(entity.attack.projectile)
        projectile.position.set(entity.position.x, entity.position.y - (entity.sprite.height / 16) + 1)
        projectile.target.set(target)

        if projectile.has('projectile'):
            projectile.projectile.parent = entity

        self.io.emit('spawn', projectile.serialize())

    def attack(self, entity, target):
        if self.world.map.distance((entity.position.x, entity.position.y), (target.position.x, target.position.y)) > 2:
            return

        entity.attack.damage(target)

class PatrolSystem(venom.System):
    def process(self, entities):
        for entity in entities.filter('patrol', '-death'):
            movement = entity.movement
            patrol = entity.patrol

            if not movement.busy() and patrol.ready():
                movement.move(*patrol.next())

class FollowSystem(venom.System):
    def process(self, entities):
        for entity in entities.filter('target', 'movement'):
            if entity.target.empty():
                continue

            target = entity.target.target

            start = entity.position.x, entity.position.y
            end = target.position.x, target.position.y

            distance = self.world.map.distance(start, end)

            if entity.has('aggro') and distance > entity.aggro.radius * 8:
                entity.target.set(None)
                entity.movement.stop()
            elif distance > 1:
                x, y = end
                entity.movement.move(x, y, 1)

class AggroSystem(venom.System):
    def process(self, entities):
        for entity in entities.filter('aggro', '-death'):
            target = entity.target

            stationary = not entity.has('movement')

            if target.empty() or stationary:
                try:
                    target.set(self.get_nearby_enemies(entity, entity.aggro.radius).next())
                except StopIteration:
                    if stationary and not target.empty():
                        target.set(None)

    def get_nearby_enemies(self, entity, radius):
        for enemy in self.world.entities.at(entity.position.x, entity.position.y, radius):
            if enemy == entity or \
               not enemy.has('health') or \
               not enemy.health.is_alive() or \
               (enemy.has('family') and entity.has('family') and enemy.family == entity.family) or \
               (enemy.has('faction') and entity.has('faction') and enemy.faction == entity.faction):
                continue

            yield enemy