entities = {}

class Entity
  constructor: (data) ->
    entities[@ata.id] = @
    @data = data

  render: ->
    @$ = $ '<div />',
      id: 'entity-' + @data.id
      class: 'entity ' + @data.kind.toLowerCase()

    @$.prependTo('#map')

  moveTo: (data) ->
    @data = data

    @$.css
      left: data.x * 12
      top: data.y * 12

    if @data.target?
      @$.addClass('attacking')
    else
      @$.removeClass('attacking')

class @Monster extends Entity

class @Player extends Entity

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
          id: "#{x}-#{y}"
          class: 'tile'

        slot.addClass('walkable') if column == 0
        slot.appendTo(map)

    $('body').html(map)

socket = io.connect "#{location.protocol}//#{location.host}",
  resource: 'socket'

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

socket.on 'move', (data) ->
  entity = entities[data.id]
  entity.moveTo(data)

socket.on 'hp', (hp) ->
  if hp == 0
    console.log 'You are dead....'
  else
    console.log 'Your HP is', hp

socket.on 'dead', (entity) ->

socket.on 'disconnect', ->
  console.log 'disconnceted'

$ ->
  $('body').on 'click', '.tile', (e) ->
    e.stopPropagation()
    e.preventDefault()
    pair = this.id.split('-')
    socket.emit('move', [parseInt(pair[0], 10), parseInt(pair[1], 10)])