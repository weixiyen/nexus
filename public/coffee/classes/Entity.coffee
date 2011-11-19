IMGPATH = '/public/img/'

GRID_W = 64
GRID_H = 32
STEP_X = 4
STEP_Y = 5

class @Entity
  STUB = 'ent-'
  constructor: (data)->

    # entity stats
    @id = data.id
    @hp = data.hp
    @kind = data.kind
    @name = data.name
    @x = data.x
    @y = data.y
    @left = @x * GRID_W
    @top = @y * GRID_H

    @target = data.target or null

  isAlive: ->
    return @hp > 0

  hasTarget: ->
    return if @target then true else false

  create: ->
    # create dom fragment and store it in the object
    @$el = $ '<div/>',
      id: STUB + @id
      class: 'entity'
      css:
        left: @left
        top: @top
        zIndex: @top

    @$elBody = $('<div/>')
      .css
        height: @height
        width: @width
        background: 'no-repeat url('+@imgurl+')'
        left: @width / 2 * -1
        top: @height * -1

    @$el.append(@$elBody)

  remove: ->
    @$el.remove()

class @MovableEntity extends Entity
  constructor: (entity)->
    super
    @speed = entity.speed || Infinity
    @moving = false
    @endLeft = @left
    @endTop = @top

  startMoving: ->
    game.addLoopItem 'unit:'+@id+':move', @speed, =>
      if !@moving then return
      @_moveTowardsGoal()

  _moveTowardsGoal: ->

    stopX = stopY = false

    changeX = STEP_X
    changeY = STEP_Y

    if @_movingDiagonally()
      changeX -= 2
      changeY -= 1

    nextLeft = @left
    nextTop = @top

    if @left > @endLeft
      nextLeft -= changeX

    if @left < @endLeft
      nextLeft += changeX

    if @top > @endTop
      nextTop -= changeY

    if @top < @endTop
      nextTop += changeY

    if Math.abs(@left - @endLeft) <= STEP_X
      nextLeft = @endLeft
      stopX = true

    if Math.abs(@top - @endTop) <= STEP_Y
      nextTop = @endTop
      stopY = true

    if stopX && stopY
      @moving = false

    @left = nextLeft
    @top = nextTop
    @$el.css
      left: @left
      top: @top
      zIndex: @top

  _movingDiagonally: ->
    if @left != @endLeft && @top != @endTop then return true
    return false

class @Monster extends MovableEntity

  constructor: (entity)->
    super
    @speed = 4
    @width = 65
    @height = 60
    @imgurl = IMGPATH + 'sprite_monster.png'

    @create()
    @startMoving()

  moveTo: (x, y)->
    @moving = true
    @endLeft = x * GRID_W
    @endTop = y * GRID_H

class @Player extends MovableEntity
  constructor: (entity)->
    super
    @speed = 3
    @width = 40
    @height = 64
    @imgurl = IMGPATH + 'sprite_user.png'

    @create()
    @startMoving()

  moveTo: (x, y)->
    @moving = true
    @endLeft = x * GRID_W
    @endTop = y * GRID_H

class @User extends MovableEntity
  constructor: (entity)->
    super
    @speed = 3
    @width = 40
    @height = 64
    @imgurl = IMGPATH + 'sprite_user.png'

    @create()