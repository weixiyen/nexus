class @GameEvents
  constructor: (options)->
    $document = $(document)
    @socket = io.connect "#{location.protocol}//#{location.host}",
      resource: 'socket'
      query: location.search.slice(1)

  connect: (fn)->
    @socket.on 'connect', ->
      fn()

  init: (fn)->
    @socket.on 'initialize', (data) ->
      fn(data)

  spawn: (fn) ->
    @socket.on 'spawn', (data) ->
      fn(data)

  move: (fn) ->
    @socket.on 'move', (data...) ->
      fn(data[0], data[1], data[2])

  death: (fn) ->
    @socket.on 'death', (data) ->
      fn(data)

  target: (fn) ->
    @socket.on 'target', (aggressorId, targetId) ->
      fn(aggressorId, targetId)

  moveMe: (x, y) ->
    @socket.emit('move', [x, y])