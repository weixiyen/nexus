socket = io.connect "#{location.protocol}//#{location.host}",
  resource: 'socket'

socket.on 'connect', ->
  console.log 'connected'

socket.on 'initialize', (state) ->
  $('body').empty()

  for x in [0...state.map.length]
    row = state.map[x]

    for y in [0...row.length]
      column = row[y]

      slot = $ '<div />',
        id: "#{x}-#{y}"
        class: 'tile'
        css:
          width: 10
          height: 10
          display: 'inline-block'
          border: '1px solid black'

      if column == 1
        slot.css('background-color', 'black')

      slot.appendTo('body')

    $('<br />').appendTo('body')

  for entity in state.entities
    color = if entity.kind is 'Player' then 'blue' else 'gray'
    $("##{entity.x}-#{entity.y}").addClass("entity-#{entity.id}").css('background-color', color)

socket.on 'spawn', (entity) ->
  color = if entity.kind is 'Player' then 'blue' else 'gray'
  $("##{entity.x}-#{entity.y}").addClass("entity-#{entity.id}").css('background-color', color)

socket.on 'move', (entity) ->
  color = if entity.target? then 'red' else 'gray'
  color = 'blue' if entity.kind is 'Player'

  $(".entity-#{entity.id}").removeClass("entity-#{entity.id}").css('background-color', 'white')
  $("##{entity.x}-#{entity.y}").css('background-color', color).addClass("entity-#{entity.id}")

socket.on 'attack', (entityId) ->
  $(".entity-#{entityId}").css('background-color', 'red')

socket.on 'hp', (hp) ->
  if hp == 0
    console.log 'You are dead....'
  else
    console.log 'Your HP is', hp

socket.on 'dead', (entity) ->
  $(".entity-#{entity.id}").removeClass("entity-#{entity.id}").css('background-color', 'white')

socket.on 'disconnect', ->
  console.log 'disconnceted'

$ ->
  $('body').on 'click', '.tile', (e) ->
    e.stopPropagation()
    e.preventDefault()
    pair = this.id.split('-')
    socket.emit('move', [parseInt(pair[0], 10), parseInt(pair[1], 10)])