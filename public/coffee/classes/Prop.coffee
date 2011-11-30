IMGPATH = '/public/img/'

GRID_W = 32
GRID_H = 16
STUB = 'prop-'

class @Prop
  constructor: (data)->
    @id = data.id
    @elementId = STUB + @id
    @kind = data.kind
    @x = data.components.position.x
    @y = data.components.position.y
    @left = @x * GRID_W
    @top = @y * GRID_H
    @width = data.components.sprite.width
    @height = data.components.sprite.height
    @imgurl = IMGPATH + data.components.sprite.src
    @create()

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