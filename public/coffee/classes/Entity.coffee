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

    @$elBody = $('<div/>')
      .css
        height: @height
        width: @width
        background: 'no-repeat url('+@imgurl+')'
        left: @width / 2 * -1
        top: @height * -1

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

    ###
    if @_movingDiagonally()
      changeX -= 2
      changeY -= 1
    ###

    # default nextLeft and nextTop values
    nextLeft = @left
    nextTop = @top

    # set nextTop and nextLeft values including direction
    if @top > @endTop
      nextTop -= changeY
      @direction = 'up'

    if @top < @endTop
      nextTop += changeY
      @direction = 'down'

    if @left > @endLeft
      nextLeft -= changeX
      @direction = 'left'

    if @left < @endLeft
      nextLeft += changeX
      @direction = 'right'

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

class @Lizard extends MovableEntity
  constructor: (entity)->
    super
    @width = 65
    @height = 60
    @animationSkip = 10
    @imgurl = IMGPATH + 'sprite_monster.png'

    @anim =
      down: [
        "0 0",
        "-65px 0",
        "-130px 0"
        ]
      up: [
        "-195px 0",
        "-260px 0",
        "-325px 0"
        ]
      left: [
        "-390px 0",
        "-455px 0",
        "-520px 0"
        ]
      right: [
        "-585px 0",
        "-650px 0",
        "-715px 0"
        ]

    @create()
    @startMoving()


class @PlayerEntity extends MovableEntity
  constructor: (entity)->
    super
    @type = 'player'
    @width = 40
    @height = 64
    @imgurl = IMGPATH + 'sprite_user.png'
    @animationSkip = 8
    @anim =
      left: [
        "0 0",
        "-50px 0",
        "-100px 0"
        ]
      up: [
        "-150px 0",
        "-200px 0",
        "-250px 0"
        ]
      down: [
        "-300px 0",
        "-350px 0",
        "-400px 0"
        ]
      right: [
        "-450px 0",
        "-500px 0",
        "-550px 0"
        ]

    @create()
    @startMoving()





class @User extends MovableEntity
  constructor: (entity)->
    super
    @type = 'user'
    @width = 40
    @height = 64
    @imgurl = IMGPATH + 'sprite_user.png'
    @animationSkip = 8
    @anim =
      left: [
        "0 0",
        "-50px 0",
        "-100px 0"
        ]
      up: [
        "-150px 0",
        "-200px 0",
        "-250px 0"
        ]
      down: [
        "-300px 0",
        "-350px 0",
        "-400px 0"
        ]
      right: [
        "-450px 0",
        "-500px 0",
        "-550px 0"
        ]

    @create()
    @startMoving()

