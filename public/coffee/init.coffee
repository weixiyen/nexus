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
  e.preventDefault()
  e.stopPropagation()
  code = e.which
  if code == 65
    game.panStart('left')
  if code == 68
    game.panStart('right')
  if code == 87
    game.panStart('up')
  if code == 83
    game.panStart('down')

$document.keyup (e)->
  e.preventDefault()
  e.stopPropagation()
  code = e.which
  if code == 65
    game.panStop('left')
  if code == 68
    game.panStop('right')
  if code == 87
    game.panStop('up')
  if code == 83
    game.panStop('down')

$(window).blur ->
  game.panStopAll()