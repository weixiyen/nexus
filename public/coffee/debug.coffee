entities = {}

class Entity
  constructor: (data) ->
    entities[data.id] = @
    @data = data
    @zIndex = @data.id

  render: ->
    @$ = $ '<div />',
      id: 'entity' + @data.id
      class: 'entity ' + @data.kind.toLowerCase()
      css:
        left: @data.x * 12
        top: @data.y * 12
        zIndex: @zIndex

    @$.prependTo('#map')

  kill: ->
    @$.remove()
    delete entities[@data.id]

  moveTo: (x, y) ->
    @data.x = x
    @data.y = y

    @$.css
      left: @data.x * 12
      top: @data.y * 12

class @Monster extends Entity
class @Turret extends Entity
class @Player extends Entity
  constructor: ->
    super
    @zIndex = @zIndex * 1000

class Map
  constructor: (@state) ->
    $('#map').remove()

  render: ->
    map = $ '<div />',
      id: 'map'
      css:
        width: 600
        height: 600

    for y in [0...@state.length]
      row = @state[y]

      for x in [0...row.length]
        column = row[x]

        slot = $ '<div />',
          data:
            x: x
            y: y
          class: 'tile'

        slot.addClass('walkable') if column == 0
        slot.appendTo(map)

    $('body').append(map)

socket = io.connect "#{location.protocol}//#{location.host}",
  resource: 'socket'
  query: location.search.slice(1)

socket.on 'connect', ->
  console.log 'connected'

socket.on 'initialize', (state) ->
  new Map(state.map).render()

  for entity in state.entities
    entity = new window[entity.kind](entity)
    entity.render()

socket.on 'spawn', (entity) ->
  entity = new window[entity.kind](entity)
  entity.render()

socket.on 'move', (id, x, y) ->
  entity = entities[id]
  entity.moveTo(x, y)

socket.on 'hp', (hp) ->
  if hp == 0
    console.log 'You are dead....'
  else
    console.log 'Your HP is', hp

socket.on 'death', (entityId) ->
  entities[entityId].kill()


socket.on 'target', (id, targetId) ->
  entity = entities[id]

  if entity.target?
    entity.$.removeClass('attacking')
  else if targetId?
    entity.$.addClass('attacking')

  entity.target = targetId

socket.on 'disconnect', ->
  console.log 'disconnceted'

$ ->
  $('body').on 'click', '.tile', (e) ->
    e.stopPropagation()
    e.preventDefault()
    data = $(this).data()
    socket.emit('move', [data.x, data.y])

  $('#spawn').on 'click', (e) ->
    socket.emit('spawn', [])