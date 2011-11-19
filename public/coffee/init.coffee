@game = new Game
  $canvas: $('#game')

@map = new Map
  $canvas: $('#map')

events = new GameEvents
  game: game
  map: map

# initialize the game canvas
events.init (data)->
  game.reset()
  map.reset()
  game.addEntities data.entities

# spawn an entity
events.spawn (entity)->
  console.log 'mob spawned', entity

# move an entity
events.move (movementData)->
  game.moveEntity movementData

events.death (entityId)->
  game.removeEntity(entityId)

$document = $(document)
$document.keydown (e)->
  code = e.which

  # left = 65
  # right = 68
  # up = 87
  # down = 83