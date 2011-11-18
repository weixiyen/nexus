class @User
  constructor: (data) ->
    @name = data.name
    @map = data.map
    @el = $('<div id="user" class="user"><div class="name">'+@name+'</div></div>').appendTo(@map.$map)
    @elName = @el.find '.name:first'
    @height = data.height
    @width = data.width
    @imgpath = data.imgpath
    @id = data.id
    @anim = data.anim
    @spriteQueue = []
    @stub = 'user-'
    @moving =
      n: false
      e: false
      s: false
      w: false

    @el.css
        height: @height
        width: @width
        background: 'no-repeat url(' + @imgpath + ')'
        position: 'fixed'
        zIndex: @map.pos[1]

    @elName.css
        left: @width / 2 - 50
        top: -10

    @tag =
      automove: 'user:path:automove'
      pathloop: 'user:path:loop'

    @center()
    @bindWindowResize()
    @face data.facing

  bindWindowResize: ->
    $(window).resize =>
      @center()

  center: ->
    left = $(window).width() / 2 - @width / 2 + @map.xOffset + 8
    top = $(window).height() / 2 - @height + @map.yOffset + 8
    @put left, top

  # relative to screen
  put: (x, y) ->
    @el.css
        left: x
        top: y

  runTo: (coords) ->

    LOOPID = @tag.pathloop
    NODE1 = 'user:path:node:1'
    NODE2 = 'user:path:node:2'

    $.loop.remove LOOPID
    @stopAll()

    xDivisor = @map.nodeWidth
    yDivisor = @map.nodeHeight
    x1 = Math.floor( @map.pos[0] / xDivisor )
    y1 = Math.floor( @map.pos[1] / yDivisor )
    x2 = Math.floor( coords[0] / xDivisor )
    y2 = Math.floor( coords[1] / yDivisor )
    path = @map.getPath [x1,y1], [x2,y2]

    # check for bad path
    if path.length < 2
      return

    # get new path segment & move the user
    run = =>
      if path.length < 2
        $.loop.remove LOOPID
        user.stopAll()
        return
      global[NODE1] = path.shift()
      global[NODE2] = path[0]
      @move @map.getDirection global[NODE1], global[NODE2]

    # GO!!!
    global[ @tag.automove ] = true
    run()

    $.loop.add LOOPID, ->
      # detect if current path segment is completed
      # if so, then stop the user, then run new direction
      if @map.completedPath global[NODE1], global[NODE2]
        user.stopAll()
        run()

  keyMove: (direction) ->

    $.loop.remove @tag.pathloop
    if global[ @tag.automove ] == true
      user.stopAll()
    global[ @tag.automove ] = false
    @move (direction)

  move: (direction) ->
    # check to see if button is already pressed
    if @moving[ direction ] == true
      return
    else
      @moving[ direction ] = true

    xBound = Math.floor( @width / 2 )
    yBound = Math.floor( @height / 2 )

    @map.panStart direction, xBound, yBound

    @stopAllSprites direction

    # begin animation
    @spriteStart @map.getSimpleDirection direction

  movingDiagonally: ->
    i = 0
    for k, v of @moving
      if v is true
        i+=1
    return i >= 2

  stop: (direction) ->
    @moving[ direction ] = false
    @map.panStop direction
    @spriteStop direction

  spriteStart: (direction) ->
    loopid = @stub + direction
    sprite.start loopid,
      el: @el
      queue: @anim[direction]
      skip: 3
    @spriteQueueAdd direction

  spriteStop: (direction) ->
    sprite.stop @stub+direction
    @spriteQueueRemove direction
    if @spriteQueue.length
      @spriteStart @spriteQueue[0]

    if global[ @tag.automove ] == false
      @face direction

  spriteQueueAdd: (direction) ->
    if !@spriteQueueHas(direction)
      @spriteQueue.push direction

  spriteQueueRemove: (direction) ->
    index = @getSpriteQueueIndex direction
    @spriteQueue.splice index, 1

  getSpriteQueueIndex: (direction) ->
    return $.inArray direction, @spriteQueue

  spriteQueueHas: (direction) ->
    -1 != @getSpriteQueueIndex direction

  stopAllSprites: (direction) ->
    for k, v of @moving
      if @moving[ k ] == true
        sprite.stop (@stub+k)

  stopAll: ->
    for k, v of @moving
      if @moving[ k ] == true
        @stop k

  teleport: (xcoord, ycoord) ->
    @map.goTo xcoord, ycoord

  face: (direction) ->
    direction = @map.getSimpleDirection direction
    @el.css
      'background-position': @anim[direction][1]
