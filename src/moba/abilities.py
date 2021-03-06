from . import buffs

def aoe(self, position):
    targets = []

    for entity in self.get_enemies_at(position, 5):
         if self.instance.map.distance(self.position, entity.position) <= 15:
             targets.append(entity)

    if targets:
        damage = (10 * self.level) / len(targets)

        for target in targets:
            target.damage_taken(self, damage)

def poison(self, target):
    if target:
        target.apply_buff(buffs.Poison, source=self)

def slow(target):
    if target:
        target.apply_buff(buffs.Slow)

def haste(target):
    if target:
        target.apply_buff(buffs.Haste)

def ultimate(self):
    for entity in self.instance.entities:
        if entity.is_alive() and entity != self:
            entity.damage_taken(self, entity.hp / 2)