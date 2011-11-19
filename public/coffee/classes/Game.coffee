class @Game

  STUB = 'ent-'
  INTERVAL = 30
  PAN_SPEED = 1
  PAN_DIST = 10
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

  reset: ->
    @$canvas.empty()
    @entities = {}

  renderOffset: ->
    style =
      left: @left
      top: @top
    @$canvas.css style
    map.$canvas.css style

  setUserId: (entityId)->
    @userId = entityId

  centerOnUser: ->
    if !@entities[STUB+@userId] then return
    me = @entities[STUB+@userId]
    @left = -me.left - me.width / 2 + $window.width() / 2
    @top = -me.top - me.height / 2 + $window.height() / 2 - UI_HEIGHT
    @renderOffset()

  addEntities: (entities)->
    for entity in entities
      @addEntity entity

  addEntity: (entityData)->
    if @entities[STUB+entityData.id] then return
    entity = null
    if entityData.id == @userId
      entity = new User(entityData)
    else if window.hasOwnProperty(entityData.kind)
      entity = new window[entityData.kind](entityData)
    if entity == null then return
    @entities[STUB+entity.id] = entity
    @addToCanvas(entity.$el)

  removeEntity: (entityId)->
    @entities[STUB+entityId].remove()
    delete @entities[ STUB + entityId ]

  moveEntity: (moveData)->
    id = moveData.id
    x = moveData.x
    y = moveData.y
    @entities[STUB+id].moveTo(x,y)

  addToCanvas: ($element)->
    @$canvas.append($element)

  beginLoop: ->
    count = 0
    setInterval =>
      if count == 999999 then count = 0
      for loopId, loopItem of @loopItems
        if count % loopItem.frequency then continue
        loopItem.fn(@loopCount)
      count += 1
    , INTERVAL

  addLoopItem: (loopId, frequency, fn) ->
    @loopItems[loopId] =
      frequency: frequency
      fn: fn

  removeLoopItem: (loopId) ->
    delete @loopItems[loopId]

  panStart: (dir)->
    if @panning[dir] then return
    @panning[dir] = true
    @addLoopItem 'pan:'+dir, PAN_SPEED, =>
      @pan(dir)

  panStop: (dir)->
    @panning[dir] = false
    @removeLoopItem('pan:'+dir)

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