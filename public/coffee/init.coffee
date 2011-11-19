game = new Game
  $canvas: $('#game')

map = new Map
  $canvas: $('#map')

events = new GameEvents

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