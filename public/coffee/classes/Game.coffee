class @Game

  STUB = 'ent-'
  PAN_SPEED = 1
  PAN_DIST = 15
  UI_HEIGHT = 50 #height of bottom interface used to center user correctly

  constructor: (options)->
    @$canvas = options.$canvas
    @loopItems = {}
    @entities = {}
    @left = 0
    @top = 0
    @userId = null
    @panning =
      left: false
      right: false
      up: false
      down: false
    @beginLoop()

  isUserId: (id)->
    return id == @userId

  beginLoop: ->
    @loopCount = 0
    gameLoop = =>
      requestAnimFrame(gameLoop)
      if @loopCount == 999999 then @loopCount = 0
      for loopId, loopItem of @loopItems
        if @loopCount % loopItem.frequency then continue
        loopItem.fn(@loopCount)
      @loopCount += 1
    gameLoop()

  reset: ->
    @$canvas.empty()
    @entities = {}

  renderOffset: ->
    style =
      left: @left
      top: @top
    @$canvas.css(style)
    map.renderOffset(style)

  setUserId: (entityId)->
    @userId = entityId

  centerOnUser: ->
    if !@entities[STUB+@userId] then return
    me = @entities[STUB+@userId]
    @left = -me.left - me.width / 2 + $window.width() / 2
    @top = -me.top - me.height / 2 + $window.height() / 2 - UI_HEIGHT
    @renderOffset()
    map.render()

  addEntities: (entities)->
    for entity in entities
      @addEntity entity

  addEntity: (entityData)->
    isUser = false
    if @entities[STUB+entityData.id] then return
    entity = null
    if entityData.id == @userId
      isUser = true
      entity = new User(entityData)
    else if window.hasOwnProperty(entityData.kind)
      entity = new window[entityData.kind](entityData)
    if entity == null then return
    if entity.hasTarget() then entity.aggro(entity.target)
    @entities[STUB+entity.id] = entity

    @addToCanvas(entity.$el)
    if isUser then @centerOnUser()

  removeEntity: (entityId)->
    @entities[STUB+entityId].remove()
    delete @entities[ STUB + entityId ]

  moveEntity: (id, x, y)->
    if !@entitiesExist(id) then return
    @entities[STUB+id].moveTo(x,y)

  target: (aggressorId, targetId)->
    if !@entitiesExist(aggressorId) then return
    entity = @entities[STUB+aggressorId]
    if targetId == null
      entity.deaggro()
      return
    entity.aggro(targetId)

  changeName: (id, name) ->
    if !@entitiesExist(id) then return
    @entities[STUB+id].changeName(name)

  damageTaken: (id, amt, isCrit) ->
    if !@entitiesExist(id) then return
    @entities[STUB+id].takeDamage(amt, isCrit)

  changeMp: (id, mp)->
    if !@entitiesExist(id) then return
    @entities[STUB+id].changeMp(mp)

  setMovementSpeed: (id, speed) ->
    if !@entitiesExist(id) then return
    @entities[STUB+id].setMovementSpeed(speed)

  entitiesExist: (ids...) ->
    for id in ids
      if !@entities[STUB+id] then return false
    return true

  userAttack: (attackType)->
    if !@entitiesExist(@userId) then return
    targetId = @entities[STUB+@userId].getTarget()
    mouseCoords = map.getMouseCoords()
    events.userAttack(attackType, targetId, mouseCoords)

  setUserTarget: (targetId)->
    if !@entitiesExist(@userId) then return
    @entities[STUB+@userId].setTarget(targetId)

  addToCanvas: ($element)->
    @$canvas.append($element)

  addLoopItem: (loopId, frequency, fn) ->
    @loopItems[loopId] =
      frequency: frequency
      fn: fn

  removeLoopItem: (loopId) ->
    delete @loopItems[loopId]

  increaseExperience: (id, amt) ->
    if !@entitiesExist(id) then return
    @entities[STUB+id].increaseExperience(amt)

  levelUp: (id, data)->
    if !@entitiesExist(id) then return
    @entities[STUB+id].levelUp(data)

  panStart: (dir)->
    if @panning[dir] then return
    @panning[dir] = true
    @addLoopItem 'pan:'+dir, PAN_SPEED, =>
      @pan(dir)
    map.startRenderLoop()

  panStop: (dir)->
    @panning[dir] = false
    @removeLoopItem('pan:'+dir)
    map.stopRenderLoop()

  panStopAll: ->
    for dir, value of @panning
      if @panning[dir] == true
        @panStop(dir)

  pan: (dir)->
    style =
      left: @left
      top: @top
    if dir == 'left'
      style.left -= PAN_DIST
    else if dir == 'right'
      style.left += PAN_DIST
    else if dir == 'up'
      style.top -= PAN_DIST
    else if dir == 'down'
      style.top += PAN_DIST

    @left = style.left
    @top = style.top

    @renderOffset()


