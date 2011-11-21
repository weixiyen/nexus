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
    @events['connect'] = fn

  init: (fn)->
    @socket.on 'initialize', fn

  spawn: (fn) ->
    @events['spawn'] = fn

  move: (fn) ->
    @events['move'] = fn

  death: (fn) ->
    @events['death'] = fn

  target: (fn) ->
    @events['target'] = fn

  mpChange: (fn)->
    @events['mp'] = fn

  xpChange: (fn)->
    @events['experience'] = fn

  levelUp: (fn)->
    @events['level-up'] = fn

  nameChange: (fn) ->
    @events['name-change'] = fn

  damageTaken: (fn) ->
    @events['damage-taken'] = fn

  setMovementSpeed: (fn) ->
    @events['set-movement-speed'] = fn

  moveMe: (x, y) ->
    @socket.emit('move', [x, y])

  userAttack: (attackType, targetId, mousePosition) ->
    @socket.emit('attack', attackType, targetId, mousePosition)
