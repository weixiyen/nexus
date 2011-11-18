class @Unit
  constructor: (data) ->

    # ATTRIBUTES
    @id = data.id
    @height = data.height
    @width = data.width
    @imgpath = data.imgpath
    @anim = data.anim
    @pos = data.pos
    @el = data.el
    @speed = data.speed
    @name = data.name
    @skip = data.skip
    @moving = false
    @tag =
      pathloop: 'unit:'+@id+':path:loop'
      node1: 'unit:'+@id+':path:node:1'
      node2: 'unit:'+@id+':path:node:2'
      move: 'unit:'+@id+':move'
      anim: 'unit:'+@id+':anim'
      chase: 'unit:'+@id+':chase'

    @elBody = @el.append('<div class="body"><div class="name"><span>'+@name+'</span></div></div>').find('.body:first')
    @elName = @el.find('.name:first')

    # METHODS
    @create()

  create: ->
    @el.css
        left: @pos[0]
        top: @pos[1]
        zIndex: @pos[1]
        height: 0
        width: 0

    @elBody.css
        height: @height
        width: @width
        background: 'no-repeat url(' + @imgpath + ')'
        left: @width / 2 * -1
        top: @height * -1

    @elName.css
        left: @width / 2 - 50
        top: -10

  stop: ->
    $.loop.remove @tag.move
    sprite.stop @tag.anim

  move: (direction) ->
    $.loop.add @tag.move, =>
      @walk direction
    sprite.start @tag.anim,
      el: @elBody
      queue: @anim[ direction ]
      skip: @skip

  walk: (direction) ->
    if direction == 'w'
      @pos[0] -= @speed
    else if direction == 'e'
      @pos[0] += @speed
    else if direction == 'n'
      @pos[1] -= @speed
    else if direction == 's'
      @pos[1] += @speed
    @el.css
        left: @pos[0]
        top: @pos[1]
        zIndex: @pos[1]

  walkTo: (coords) ->

    LOOPID = @tag.pathloop
    NODE1 = @tag.node1
    NODE2 = @tag.node2

    $.loop.remove LOOPID
    @stop()

    xDivisor = map.nodeWidth
    yDivisor = map.nodeHeight
    x1 = Math.floor( @pos[0] / xDivisor )
    y1 = Math.floor( @pos[1] / yDivisor )
    x2 = Math.floor( coords[0] / xDivisor )
    y2 = Math.floor( coords[1] / yDivisor )
    path = map.getPath [x1,y1], [x2,y2]

    # check for bad path
    if path.length < 2
      return

    # get new path segment & move the user
    walk = =>
      if path.length < 2
        $.loop.remove LOOPID
        @stop()
        return
      global[NODE1] = path.shift()
      global[NODE2] = path[0]
      @move map.getDirection global[NODE1], global[NODE2]

    walk()

    $.loop.add LOOPID, =>
      # detect if current path segment is completed
      # if so, then stop the user, then run new direction
      if map.completedPath global[NODE1], global[NODE2], [@pos[0], @pos[1]]
        @stop()
        walk()

  doAbility: ->
    console.log 'do ability'

  teleport: ->
    console.log 'teleport'

  show: ->
    console.log 'show'

  remove: ->
    console.log 'remove'

  target: (id)->
    console.log 'target'

  chase: ( obj ) ->

    if !( obj instanceof Unit )
      obj = map

    $.loop.add @tag.chase, 35, =>
      @walkTo obj.pos

  stopChase: ->
    $.loop.stop @tag.chase
    @stop()

class @PC extends @Unit
  eat: ->
    console.log 'fooofofo'

class @NPC extends @Unit
  eat: ->
    console.log 'eat'