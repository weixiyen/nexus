IMGPATH = '/public/img/'

GRID_W = 32
GRID_H = 16
STUB = 'prop-'

class @Prop
  constructor: (data)->
    @id = data.id
    @elementId = STUB + @id
    @kind = data.kind
    @x = data.x
    @y = data.y
    @left = @x * GRID_W
    @top = @y * GRID_H
    @width = data.sprite.width
    @height = data.sprite.height
    @imgurl = IMGPATH + data.sprite.src

  create: ->
    if !@bgPos then @bgPos = '0 0'
    if !@topOffset then @topOffset = 0

    @$el = $ '<div/>',
      id: @elementId
      class: 'prop'
      css:
        left: @left - @width / 2
        top: @top - @height
        width: @width
        height: @height
        zIndex: @top
        background: 'no-repeat url('+@imgurl+') '+ @bgPos
      data:
        prop: @

class @Tree extends Prop
  constructor: (data)->
    super
    @create()

class @Rock extends Prop
  constructor: (data)->
    super
    @create()
