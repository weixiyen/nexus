IMGPATH = '/public/img/'

GRID_W = 32
GRID_H = 16
STEP_X = 5
STEP_Y = 3

class @Entity
  STUB = 'ent-'
  constructor: (data)->
    # entity stats
    @id = data.id
    @hp = data.hp
    @kind = data.kind
    @name = data.name
    @stats = data.stats
    @x = data.x
    @y = data.y
    @left = @x * GRID_W
    @top = @y * GRID_H
    @sprite = null
    @bodyOffset = 0

    @target = data.target or null
    @type = 'unit'

  isAlive: ->
    return @hp > 0

  hasTarget: ->
    return if @target then true else false

  create: ->
    # create dom fragment and store it in the object
    @$el = $ '<div/>',
      id: STUB + @id
      class: 'entity '+@type
      css:
        left: @left
        top: @top
        zIndex: @top
      data:
        entity: @

    @$elBody = $ '<div/>',
      class: 'body'
      css:
        height: @height
        width: @width
        background: 'no-repeat url('+@imgurl+')'
        left: @bodyOffset

    @$elName = $ '<div/>',
      class: 'name'
      css:
        left: @width / 2 - 50
        top: -25
    @$elName.html(@name)

    @$elBar = $ '<div/>',
      class: 'bar br2'
      css:
        left: @width / 2 - 25
        top: -10

    @$elHp = $ '<div/>',
      class: 'hp br2'

    @$elBar.append(@$elHp)

    @$el.append(@$elName, @$elBar, @$elBody)

    @setHp(@hp)

  setTarget: (targetId)->
    @target = targetId

  getTarget: ->
    return @target

  remove: ->
    @$el.remove()

  setCoords: ->
    @x = Math.floor(@left / GRID_W)
    @y = Math.floor(@top / GRID_H)

  aggro: (id)->
    @target = id
    @$elName.addClass('red')

  deaggro: ->
    @target = null
    @$elName.removeClass('red')

  changeName: (name)->
    @name = name
    @$elName.html(name)

  takeDamage: (amt, isCrit)->
    @setHp(@hp - amt)

  setMovementSpeed: (speed)->
    game.removeLoopItem 'unit:'+@id+':move'
    @speed = speed
    @startMoving()

  setHp: (hp)->
    @hp = hp
    perc = Math.ceil(@hp / @stats.hp * 100) + '%'
    @$elHp.css
      width: perc


class @MovableEntity extends Entity
  constructor: (entity)->
    super
    @speed = entity.movement_speed || 1
    @moving = false
    @endLeft = @left
    @endTop = @top
    @curDir = null #current direction

  startMoving: ->
    game.addLoopItem 'unit:'+@id+':move', @speed, =>
      if !@moving then return
      @_moveTowardsGoal()

  _moveTowardsGoal: ->

    stopX = stopY = false
    @direction = null

    changeX = STEP_X
    changeY = STEP_Y

    if @_movingDiagonally()
      changeX -= 2
      changeY -= 1

    # default nextLeft and nextTop values
    nextLeft = @left
    nextTop = @top

    # set nextTop and nextLeft values including direction
    if @top > @endTop
      nextTop -= changeY
      @direction = 'n'

    if @top < @endTop
      nextTop += changeY
      @direction = 's'

    if @left > @endLeft
      nextLeft -= changeX
      if @direction != null
        @direction += 'w'
      else
        @direction = 'w'

    if @left < @endLeft
      nextLeft += changeX
      if @direction != null
        @direction += 'e'
      else
        @direction = 'e'

    # if end point less than the change amount, just have mob jump to end point
    if Math.abs(@left - @endLeft) <= STEP_X
      nextLeft = @endLeft
      stopX = true

    if Math.abs(@top - @endTop) <= STEP_Y
      nextTop = @endTop
      stopY = true

    # if mob is not moving, set moving to false and direction to null
    if stopX && stopY
      @moving = false
      @direction = null

    @left = nextLeft
    @top = nextTop
    @$el.css
      left: @left
      top: @top
      zIndex: @top

    # animate sprite when moving
    @walk()

  _movingDiagonally: ->
    if @left != @endLeft && @top != @endTop then return true
    return false

  walk: ->

    if @curDir == @direction then return

    if @sprite
      @sprite.stop(@id)
    else
      @sprite = new Sprite
        id: @id
        el: @$elBody
        skip: @animationSkip

    @curDir = @direction

    if @curDir == null then return
    skip = @animationSkip
    if @curDir == 'down' || @curDir == 'up'
      skip = Math.round(skip / 1.5)
    @sprite.start(@anim[@curDir], skip)

  moveTo: (x, y)->
    @moving = true
    @endLeft = x * GRID_W - Math.floor(@width / 2)
    @endTop = y * GRID_H - Math.floor(@height / 2)


class @Turret extends Entity
  constructor: (entity)->
    super
    @width = 96
    @height = 96
    @imgurl = IMGPATH + 'turret.png'
    @create()

class @Minion extends MovableEntity
  constructor: (entity)->
    super
    @bodyOffset = 2
    @width = 48
    @height = 60
    @animationSkip = 8
    @imgurl = IMGPATH + 'sprite_robot.png'

    @anim =
      n: [
        "-50px 0",
        "-716px 0",
        "-776px 0",
        "-836px 0",
        "-896px 0",
        "-956px 0",
        "-1016px 0"
        ]
      s: [
        "-207px 0"
        "-1766px 0",
        "-1824px 0",
        "-1883px 0",
        "-1941px 0",
        "-1999px 0",
        "-2058px 0"
        ]
      w: [
        "-360px 0",
        "-2752px 0",
        "-2803px 0",
        "-2859px 0",
        "-2910px 0",
        "-2959px 0",
        "-3009px 0"
        ]
      e: [
        "0 0",
        "-410px 0",
        "-461px 0",
        "-517px 0",
        "-568px 0",
        "-617px 0",
        "-667px 0"
        ]
      ne: [
        "-107px 0",
        "-1076px 0",
        "-1132px 0",
        "-1184px 0",
        "-1239px 0",
        "-1299px 0",
        "-1362px 0"
        ]
      se: [
        "-264px 0",
        "-2116px 0",
        "-2171px 0",
        "-2231px 0",
        "-2286px 0",
        "-2335px 0",
        "-2384px 0"
        ]
      nw: [
        "-157px 0",
        "-1421px 0",
        "-1477px 0",
        "-1529px 0",
        "-1584px 0",
        "-1644px 0",
        "-1707px 0"
        ]
      sw: [
        "-312px 0",
        "-2434px 0",
        "-2489px 0",
        "-2549px 0",
        "-2604px 0",
        "-2653px 0",
        "-2702px 0"
        ]

    @create()
    @startMoving()


class @PlayerEntity extends MovableEntity
  constructor: (entity)->
    super
    @type = 'user'
    @width = 28
    @bodyOffset = 4
    @height = 50
    @imgurl = IMGPATH + 'sprite_ryu.png'
    @animationSkip = 4
    @anim =
      n: [
        "-63px 0",
        "-482px 0",
        "-515px 0",
        "-548px 0",
        "-581px 0",
        "-614px 0",
        "-647px 0"
        ]
      s: [
        "-155px 0",
        "-1090px 0",
        "-1122px 0",
        "-1155px 0",
        "-1188px 0",
        "-1220px 0",
        "-1253px 0"
        ]
      w: [
        "-253px 0",
        "-1696px 0",
        "-1733px 0",
        "-1766px 0",
        "-1797px 0",
        "-1833px 0",
        "-1865px 0"
        ]
      e: [
        "0 0",
        "-282px 0",
        "-319px 0",
        "-352px 0",
        "-383px 0",
        "-419px 0",
        "-451px 0"
        ]
      ne: [
        "-97px 0",
        "-680px 0",
        "-717px 0",
        "-749px 0",
        "-783px 0",
        "-821px 0",
        "-853px 0"
        ]
      se: [
        "-189px 0",
        "-1286px 0",
        "-1322px 0",
        "-1355px 0",
        "-1389px 0",
        "-1425px 0",
        "-1459px 0"
        ]
      nw: [
        "-126px 0",
        "-885px 0",
        "-922px 0",
        "-954px 0",
        "-988px 0",
        "-1026px 0",
        "-1058px 0"
        ]
      sw: [
        "-221px 0",
        "-1491px 0",
        "-1527px 0",
        "-1560px 0",
        "-1594px 0",
        "-1630px 0",
        "-1664px 0"
        ]

    @create()
    @startMoving()


class @User extends MovableEntity
  constructor: (entity)->
    super
    @type = 'user'
    @width = 28
    @bodyOffset = 4
    @height = 50
    @imgurl = IMGPATH + 'sprite_ryu.png'
    @animationSkip = 4
    @anim =
      n: [
        "-63px 0",
        "-482px 0",
        "-515px 0",
        "-548px 0",
        "-581px 0",
        "-614px 0",
        "-647px 0"
        ]
      s: [
        "-155px 0",
        "-1090px 0",
        "-1122px 0",
        "-1155px 0",
        "-1188px 0",
        "-1220px 0",
        "-1253px 0"
        ]
      w: [
        "-253px 0",
        "-1696px 0",
        "-1733px 0",
        "-1766px 0",
        "-1797px 0",
        "-1833px 0",
        "-1865px 0"
        ]
      e: [
        "0 0",
        "-282px 0",
        "-319px 0",
        "-352px 0",
        "-383px 0",
        "-419px 0",
        "-451px 0"
        ]
      ne: [
        "-97px 0",
        "-680px 0",
        "-717px 0",
        "-749px 0",
        "-783px 0",
        "-821px 0",
        "-853px 0"
        ]
      se: [
        "-189px 0",
        "-1286px 0",
        "-1322px 0",
        "-1355px 0",
        "-1389px 0",
        "-1425px 0",
        "-1459px 0"
        ]
      nw: [
        "-126px 0",
        "-885px 0",
        "-922px 0",
        "-954px 0",
        "-988px 0",
        "-1026px 0",
        "-1058px 0"
        ]
      sw: [
        "-221px 0",
        "-1491px 0",
        "-1527px 0",
        "-1560px 0",
        "-1594px 0",
        "-1630px 0",
        "-1664px 0"
        ]


    @create()
    @startMoving()

###
class @User extends MovableEntity
  constructor: (entity)->
    super
    @type = 'user'
    @width = 40
    @height = 64
    @imgurl = IMGPATH + 'sprite_user.png'
    @animationSkip = 8
    @anim =
      w: [
        "0 0",
        "-50px 0",
        "-100px 0"
        ]
      n: [
        "-150px 0",
        "-200px 0",
        "-250px 0"
        ]
      s: [
        "-300px 0",
        "-350px 0",
        "-400px 0"
        ]
      e: [
        "-450px 0",
        "-500px 0",
        "-550px 0"
        ]

    @create()
    @startMoving()

###