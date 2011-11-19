class @GameEvents
  constructor: ->
    @socket = io.connect "#{location.protocol}//#{location.host}",
      resource: 'socket'

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
    @socket.on 'move', (data) ->
      fn(data)