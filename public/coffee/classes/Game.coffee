class @Game

  STUB = 'ent-'
  INTERVAL = 30

  constructor: (options)->
    @$canvas = options.$canvas
    @entities = {}
    @beginLoop()

  reset: ->
    @$canvas.empty()
    @entities = {}

  addEntities: (entities)->
    for entity in entities
      @addEntity entity

  addEntity: (entityData)->
    entity = null
    if window.hasOwnProperty(entityData.kind)
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
      for entityId, entity of @entities
        entity.nextIteration(count)
      count += 1
    , INTERVAL

  registerLoop: ->