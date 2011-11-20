window.entities = {}

class Entity
  constructor: (data) ->
    window.entities[data.id] = @
    @data = data
    @color = 'gray'
    @queue = []

  render: (ctx) ->
    return if @dead

    if (@queue.length)
      [@data.x, @data.y] = @queue.shift()

    ctx.fillStyle = if @data.target? then 'red' else @color
    ctx.fillRect(@data.x * 10, @data.y * 10, 10, 10)

  kill: ->
    @dead = true
    delete window.entities[@data.id]

  moveTo: (x, y) ->
    @queue.push([x, y])

class @Monster extends Entity
class @Turret extends Entity
  constructor: ->
    super
    @color = 'purple'

class @Player extends Entity
  constructor: ->
    super
    @color = 'blue'

class Map
  constructor: (@state) ->

  render: (ctx) ->
    for y in [0...@state.length]
      row = @state[y]

      for x in [0...row.length]
        column = row[x]

        if column == 1
          ctx.fillStyle = 'black'
          ctx.fillRect(x * 10 , y * 10, 10, 10)

socket = io.connect "#{location.protocol}//#{location.host}",
  resource: 'socket'

socket.on 'connect', ->
  console.log 'connected'

socket.on 'initialize', (state) ->
  canvas = $('canvas')[0]
  ctx = canvas.getContext('2d')

  window.entities ={}

  map = new Map(state.map)

  for entity in state.entities
    new window[entity.kind](entity)

  render = ->
    window.webkitRequestAnimationFrame(render)

    ctx.clearRect(0, 0 , 600, 600)

    map.render(ctx)

    for _, entity of window.entities
      entity.render(ctx)

  window.webkitRequestAnimationFrame(render)

socket.on 'spawn', (entity) ->
  entity = new window[entity.kind](entity)
  entity.render($('canvas')[0].getContext('2d'))

socket.on 'move', (entityId, x, y) ->
  entity = entities[entityId]
  entity.moveTo(x, y)

socket.on 'target', (id, targetId) ->
  entity = entities[id]
  entity.data.target = targetId

socket.on 'hp', (hp) ->
  if hp == 0
    console.log 'You are dead....'
  else
    console.log 'Your HP is', hp

socket.on 'death', (entityId) ->
  entities[entityId].kill()

socket.on 'disconnect', ->
  console.log 'disconnceted'

$ ->
  $('canvas').on 'click', (e) ->
    e.stopPropagation()
    e.preventDefault()
    socket.emit('move', [Math.round(e.offsetX / 10), Math.round(e.offsetY / 10)])

  $('#spawn').on 'click', (e) ->
    socket.emit('spawn', [])