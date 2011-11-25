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
    @mp = data.mp
    @kind = data.kind
    @name = data.name
    @level = data.level
    @stats = data.stats
    @experience = data.experience
    @width = data.sprite.width
    @height = data.sprite.height
    @imgurl = IMGPATH + data.sprite.src
    @animate = data.sprite.animate
    @x = data.x
    @y = data.y
    @left = @x * GRID_W
    @top = @y * GRID_H
    @sprite = null
    @suppressInfo = false
    @hitsTaken = 0
    @zIndexAdjustment = 0

    @target = data.target or null
    @type = 'unit'

    if @animate['walk']
      @anim = {}

      for direction, i in ['nw', 'n', 'ne', 'w', 'e', 'sw' ,'s' ,'se']
        frames = @animate['walk'] + @animate['stand']

        @anim[direction] = directions = []

        for frame in [0...frames]
          directions.push("-#{frame * @width}px -#{i * @height}px")

  isAlive: ->
    return @hp > 0

  hasTarget: ->
    return if @target then true else false

  userTargeted: ->
    imgurl = IMGPATH + 'target_arrow.png'
    @$targetArrow = $('<div/>').css
      background: 'url('+imgurl+') no-repeat'
      height: 10
      width: 10
      position: 'absolute'
      left: @width / 2 - 5
      top: -35
    @$el.addClass('targeted')
    @$elBody.prepend(@$targetArrow)

  removeUserTarget: ->
    @$el.removeClass('targeted')
    @$targetArrow.remove()

  create: ->

    # create dom fragment and store it in the object
    @$el = $ '<div/>',
      id: STUB + @id
      class: 'entity '+@type
      css:
        left: @left
        top: @top
        zIndex: @top + @zIndexAdjustment
      data:
        entity: @

    @$elBody = $ '<div/>',
      class: 'body'
      css:
        height: @height
        width: @width
        background: 'no-repeat url('+@imgurl+')'
        left: -Math.ceil(@width / 2)
        top: -@height
        position: 'absolute'

    if !@suppressInfo
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
      @$elBody.append(@$elName, @$elBar)
    @$el.append(@$elBody)

    @setHp(@hp)

  setTarget: (targetId)->
    @target = targetId

  getTarget: ->
    return @target

  remove: ->
    #@gotKilledEffect()
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
    if game.isUserId(@id) then interface.setName(@name)

  heal: (amt)->
    @setHp(@hp + amt)

  takeDamage: (amt, isCrit)->
    @setHp(@hp - amt)
    @gotHitEffect(isCrit)

  setMovementSpeed: (speed)->
    game.removeLoopItem 'unit:'+@id+':move'
    @speed = speed
    @startMoving()

  setHp: (hp)->
    @hp = hp
    perc = Math.ceil(@hp / @stats.hp * 100)
    @$elHp.css
      width: perc + '%'

    if game.isUserId(@id) then interface.setHp(perc)

  changeMp: (amt)->
    @setMp(@mp + amt)

  setMp: (mp)->
    @mp = mp
    perc = Math.ceil(@mp / @stats.mp * 100)
    if !game.isUserId(@id) then return
    interface.setMp(perc)
    interface.renderAbilityIconsByMp(@mp)

  increaseExperience: (amt)->
    @experience.have += amt
    perc = Math.ceil(@experience.have / @experience.need * 100)
    if !game.isUserId(@id) then return
    interface.setXp(perc)

  levelUp: (data)->
    @stats = data.stats
    @experience = data.experience
    @increaseExperience(0)
    @setHp(data.hp)
    @setMp(data.mp)
    @setLevel(data.level)

  setLevel: (level)->
    @level = level
    if game.isUserId(@id) then interface.setLevel(@level)

  gotHitEffect: (isCrit)->
    @hitsTaken += 1
    stub = 'dmg:effect:'+@id+':'+@hitsTaken

    # create dom fragment
    if @suppressInfo == true then return
    bgPos = '0 0'
    if isCrit then bgPos = '-66px 0'
    imgurl = IMGPATH + 'sprite_explosion_yellow.png'
    $explosion = $('<div/>').css
      background: 'url('+imgurl+') no-repeat ' + bgPos
      height: 66
      width: 66
      position: 'absolute'
      left: Math.round(@width / 2) - 33
      top: 0
      zIndex: 100
    @$elBody.prepend($explosion)

    # remove it from DOM on next loop iteration

    game.addLoopItem stub, 15, ->
      $explosion.remove()
      game.removeLoopItem(stub)

  gotKilledEffect: ->
    @hitsTaken += 1
    stub = 'dmg:effect:'+@id+':'+@hitsTaken
    # create dom fragment
    if @suppressInfo == true then return
    bgPos = '-132px 0'
    imgurl = IMGPATH + 'sprite_explosion_yellow.png'
    $explosion = $('<div/>').css
      background: 'url('+imgurl+') no-repeat ' + bgPos
      height: 66
      width: 66
      position: 'absolute'
      left: @left + -Math.ceil(@width / 2) + Math.round(@width / 2) - 33
      top: @top - @height
      zIndex: @top+100
    game.$canvas.append($explosion)

    # remove it from DOM on next loop iteration
    game.addLoopItem stub, 15, ->
      $explosion.remove()
      game.removeLoopItem(stub)

class @MovableEntity extends Entity
  constructor: (entity)->
    super
    @speed = entity.movement_speed || 1
    @moving = false
    @endLeft = @left
    @endTop = @top
    @curDir = null #current direction

  startMoving: ->
    @sprite = new Sprite
      id: @id
      el: @$elBody
      skip: @animationSkip
    @faceRandomDirection()
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

    prevDir = @curDir

    if @curDir == @direction then return

    @sprite.stop(@id)

    @curDir = @direction

    if @curDir == null then return @standFacing(prevDir)
    skip = @animationSkip
    if @curDir == 'down' || @curDir == 'up'
      skip = Math.round(skip / 1.5)
    @sprite.start(@anim[@curDir], skip)

  moveTo: (x, y)->
    @moving = true
    @endLeft = x * GRID_W - Math.round(@width / 2) + Math.round(GRID_W / 2)
    @endTop = y * GRID_H - Math.round(@height / 2) + GRID_H * 2

  standFacing: (direction)->
    @sprite.set(@anim[direction][0])

  faceRandomDirection: ->
    dirList = ['n','e','s','w','nw','ne','sw','se']
    direction = dirList[random(0,7)]
    @standFacing(direction)

class @Tower extends Entity
  constructor: (entity)->
    super
    @create()

class @Nexus extends Entity
  constructor: (entity)->
    super
    @zIndexAdjustment = -@height + 60
    @create()

class @Minion extends MovableEntity
  constructor: (entity)->
    super
    @animationSkip = 8
    @create()
    @startMoving()

class @PlayerEntity extends MovableEntity
  constructor: (entity)->
    super
    @type = 'user'
    @animationSkip = 4
    @create()
    @startMoving()


class @User extends MovableEntity
  constructor: (entity)->
    super
    @type = 'user'
    @animationSkip = 4
    @create()
    @startMoving()
    @setupInterface()

  setupInterface: ->
    @increaseExperience(0)
    @setLevel(@level)
    @changeName(@name)

class @TowerAttack extends MovableEntity
  constructor:(entity)->
    super
    @animationSkip = 2
    @suppressInfo = true

    @anim =
      n: [
        "0 -198px",
        "-33px -198px",
        "-66px -198px"
        ]
      s: [
        "0 -66px",
        "-33px -66px",
        "-66px -66px"
        ]
      w: [
        "0 0",
        "-33px 0",
        "-66px 0"
        ]
      e: [
        "0 -132px",
        "-33px -132px",
        "-66px -132px"
        ]
      ne: [
        "0 -165px",
        "-33px -165px",
        "-66px -165px"
        ]
      se: [
        "0 -99px",
        "-33px -99px",
        "-66px -99px"
        ]
      nw: [
        "0 -231px",
        "-33px -231px",
        "-66px -231px"
        ]
      sw: [
        "0 -33px",
        "-33px -33px",
        "-66px -33px"
        ]

    @create()
    @startMoving()

  setHp: ->
    return null

  aggro: ->
    return null

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