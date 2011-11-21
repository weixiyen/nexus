@$document = $(document)
@$window = $(window)

@game = new Game
  $canvas: $('#game')

@map = new Map
  $canvas: $('#map')

@events = new GameEvents
  game: game
  map: map

@interface = new Interface
  $canvas: $('#interface')

# initialize the game canvas
events.init (data)->
  game.reset()
  map.reset()
  map.setup(data.map)
  game.setUserId(data.me)
  game.addEntities(data.entities)

# spawn an entity
events.spawn (entity)->
  game.addEntity entity

# move an entity
events.move (id, x, y)->
  game.moveEntity(id, x, y)

events.death (entityId)->
  game.removeEntity(entityId)

events.target (aggressorId, targetId) ->
  game.target(aggressorId, targetId)

events.nameChange (id, name)->
  game.changeName(id, name)

events.damageTaken (id, amt, isCrit) ->
  game.damageTaken(id, amt, isCrit)

events.setMovementSpeed (id, speed) ->
  game.setMovementSpeed(id, speed)

events.mpChange (id, mp)->
  game.changeMp(id, mp)

events.xpChange (id, xp)->
  game.increaseExperience(id, xp)

events.levelUp (id, data)->
  game.levelUp(id, data)


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

  # panning stop
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

  # user abilities
  if code == 81 # Q
    captured = true
    game.userAttack(1)
  if code == 69 # E
    captured = true
    game.userAttack(2)
  if code == 82 # R
    captured = true
    game.userAttack(3)
  if code == 70 # F
    captured = true
    game.userAttack(4)

  if captured == true
    e.preventDefault()
    e.stopPropagation()

game.$canvas.on 'click', '.entity', (e)->
  entity = $(@).data('entity')
  game.setUserTarget(entity.id)
  events.userAttack(0, entity.id, [map.getMouseCoords()])

$window.on 'blur', ->
  game.panStopAll()

$window.on 'resize', (e)->
  interface.reload()
  map.setClientDimensions()