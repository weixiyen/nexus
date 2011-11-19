@$document = $(document)
@$window = $(window)

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
  game.setUserId(data.me)
  game.addEntities(data.entities)
  game.centerOnUser()

# spawn an entity
events.spawn (entity)->
  game.addEntity entity

# move an entity
events.move (movementData)->
  game.moveEntity(movementData)

events.death (entityId)->
  game.removeEntity(entityId)

$document.keydown (e)->
  e.preventDefault()
  e.stopPropagation()
  code = e.which
  if code == 65
    game.panStart('right')
  if code == 68
    game.panStart('left')
  if code == 87
    game.panStart('down')
  if code == 83
    game.panStart('up')
  if code == 32
    game.centerOnUser()

$document.keyup (e)->
  e.preventDefault()
  e.stopPropagation()
  code = e.which
  if code == 65
    game.panStop('right')
  if code == 68
    game.panStop('left')
  if code == 87
    game.panStop('down')
  if code == 83
    game.panStop('up')

$window.blur ->
  game.panStopAll()