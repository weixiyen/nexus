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
      @data = @queue.shift()

    ctx.fillStyle = if self.target? then 'red' else @color
    ctx.fillRect(@data.x * 10, @data.y * 10, 10, 10)

  kill: ->
    @dead = true
    delete window.entities[@data.id]

  moveTo: (data) ->
    @queue.push(data)

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

        if column == 0
          ctx.fillStyle = 'white'
          ctx.fillRect(x * 10 , y * 10, 10, 10)
          ctx.strokeStyle = 'black'
          ctx.strokeRect(x * 10 , y * 10, 10, 10)
        else
          ctx.fillStyle = 'black'
          ctx.fillRect(x * 10 , y * 10, 10, 10)

socket = io.connect "#{location.protocol}//#{location.host}",
  resource: 'socket'

socket.on 'connect', ->
  console.log 'connected'

socket.on 'initialize', (state) ->
  ctx = $('canvas')[0].getContext('2d')

  window.entities ={}

  map = new Map(state.map)

  for entity in state.entities
    new window[entity.kind](entity)

  render = ->
    map.render(ctx)

    for _, entity of window.entities
      entity.render(ctx)

    window.webkitRequestAnimationFrame(render)

  window.webkitRequestAnimationFrame(render)

socket.on 'spawn', (entity) ->
  entity = new window[entity.kind](entity)
  entity.render($('canvas')[0].getContext('2d'))

socket.on 'move', (data) ->
  entity = entities[data.id]
  entity.moveTo(data)

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