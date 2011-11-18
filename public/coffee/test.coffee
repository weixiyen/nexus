socket = io.connect 'http://localhost:8888',
  resource: 'socket'

socket.on 'connect', ->
  console.log 'connected'

socket.on 'game:init', (state) ->
  for x in [0...state.map.length]
    row = state.map[x]

    for y in [0...row.length]
      column = row[y]

      slot = $ '<div />',
        id: "#{x}-#{y}"
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
    $("##{entity.x}-#{entity.y}").addClass("entity-#{entity.id}").css('background-color', 'green')

socket.on 'move', (entity) ->
  $(".entity-#{entity.id}").removeClass("entity-#{entity.id}").css('background-color', 'white')
  $("##{entity.x}-#{entity.y}").css('background-color', 'green').addClass("entity-#{entity.id}")

socket.on 'dead', (entity) ->
  $(".entity-#{entity.id}").removeClass("entity-#{entity.id}").css('background-color', 'white')

socket.on 'log', (message) ->
  console.log(message)

socket.on 'message', (message) ->
  console.log message

socket.on 'disconnect', ->
  console.log 'disconnceted'