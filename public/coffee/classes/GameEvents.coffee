class @GameEvents
  constructor: (options)->
    $document = $(document)
    @socket = io.connect "#{location.protocol}//#{location.host}",
      resource: 'socket'
      query: location.search.slice(1)

    @events = {}

    @socket.on 'instructions', (instructions) =>
      instructions = JSON.parse(instructions)

      for instruction in instructions
        [event, data] = instruction
        try
          @events[event].apply(@, data)
        catch e
          console.log(event, data)

  connect: (fn)->
    @events['connect'] = ->
      fn()

  init: (fn)->
    @socket.on 'initialize', (data) ->
      fn(data)

  spawn: (fn) ->
    @events['spawn'] = (data) ->
      fn(data)

  move: (fn) ->
    @events['move'] = (data...) ->
      fn(data[0], data[1], data[2])

  death: (fn) ->
    @events['death'] = (data) ->
      fn(data)

  target: (fn) ->
    @events['target'] = (aggressorId, targetId) ->
      fn(aggressorId, targetId)

  mpChange: (fn)->
    @events['mp'] = (id, mp)->
      fn(id, mp)

  nameChange: (fn) ->
    @events['name-change'] = (id, name) ->
      fn(id, name)

  damageTaken: (fn) ->
    @events['damage-taken'] = (id, amt, isCritical) ->
      fn(id, amt, isCritical)

  setMovementSpeed: (fn) ->
    @events['set-movement-speed'] = (id, speed) ->
      fn(id, speed)

  moveMe: (x, y) ->
    @socket.emit('move', [x, y])

  userAttack: (attackType, targetId, mousePosition) ->
    @socket.emit('attack', attackType, targetId, mousePosition)