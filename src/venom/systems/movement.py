import venom

class MovementSystem(venom.System):
    def process(self, entities):
        for entity in entities.filter('movement'):
            movement = entity.movement

            if movement.ready():
                position = entity.position
                position.x, position.y = movement.queue.pop()
                self.io.emit('move', entity.id, position.x, position.y)