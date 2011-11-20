@$document = $(document)
@$window = $(window)

@game = new Game
  $canvas: $('#game')

@map = new Map
  $canvas: $('#map')

@events = new GameEvents
  game: game
  map: map

# initialize the game canvas
events.init (data)->
  game.reset()
  map.reset()
  map.setup(data.map)
  game.setUserId(data.me)
  game.addEntities(data.entities)
  game.centerOnUser()


# spawn an entity
events.spawn (entity)->
  game.addEntity entity

# move an entity
events.move (id, x, y)->
  game.moveEntity(id, x, y)

events.death (entityId)->
  game.removeEntity(entityId)

$document.on 'keydown', (e)->
  captured = false
  code = e.which
  if code == 65
    captured = true
    game.panStart('right')
  if code == 68
    captured = true
    game.panStart('left')
  if code == 87
    captured = true
    game.panStart('down')
  if code == 83
    captured = true
    game.panStart('up')
  if code == 32
    captured = true
    game.centerOnUser()
  if captured == true
    e.preventDefault()
    e.stopPropagation()

$document.on 'keyup', (e)->
  captured = false
  code = e.which
  if code == 65
    captured = true
    game.panStop('right')
  if code == 68
    captured = true
    game.panStop('left')
  if code == 87
    captured = true
    game.panStop('down')
  if code == 83
    captured = true
    game.panStop('up')
  if captured == true
    e.preventDefault()
    e.stopPropagation()



$window.on 'blur', ->
  game.panStopAll()

