import buff

def aoe(self, coordinates):
    targets = []

    for entity in self.get_entities_at(coordinates, 5):
         if self.instance.map.get_distance(self, entity) <= 15:
             targets.append(entity)

    if targets:
        damage = (10 * self.level) / len(targets)

        for target in targets:
            target.damage_taken(self, damage)

def poison(self, target):
    if target:
        target.apply_buff(buff.Poison, source=self)

def slow(target):
    if target:
        target.apply_buff(buff.Slow)

def haste(target):
    if target:
        target.apply_buff(buff.Haste)

def ultimate(self):
    for entity in self.instance.entities:
        if entity.is_alive() and entity != self:
            entity.damage_taken(self, entity.hp / 2)