import venom

class Collision(venom.Component):
    def update(self):
        position = self.entity.position
        sprite = self.entity.sprite
        self.entity.world.map.add_collision(position.x, position.y, sprite.width, sprite.height / 1.8)