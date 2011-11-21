IMGPATH = '/public/img/'

GRID_W = 32
GRID_H = 16
STUB = 'prop-'

class @Prop
  constructor: (data)->
    @id = data.id
    @kind = data.kind
    @x = data.x
    @y = data.y
    @left = @x * GRID_W
    @top = @y * GRID_H

  create: ->
    if !@bgPos then @bgPos = '0 0'

    @$el = $ '<div/>',
      id: STUB + @id
      class: 'prop '+@type
      css:
        left: @left - @width / 2
        top: @top - @height / 2
        width: @width
        height: @height
        zIndex: @top
        background: 'no-repeat url('+@imgurl+') '+ @bgPos
      data:
        prop: @

class @Tree extends Prop
  constructor: (data)->
    super
    @height = 300
    @width = 300
    @type = data.type
    @imgurl = IMGPATH + 'sprite_tree.png'
    @create()

class @Rock extends Prop
  constructor: (data)->
    super
    @height = 150
    @width = 150
    @type = data.type
    @imgurl = IMGPATH + 'sprite_rock.png'
    @create()

class @Tree1 extends Tree
  constructor: (data)->
    @bgPos = '0 0'
    super

class @Tree2 extends Tree
  constructor: (data)->
    @bgPos = '-300px 0'
    super

class @Tree3 extends Tree
  constructor: (data)->
    @bgPos = '-600px 0'
    super

class @Tree4 extends Tree
  constructor: (data)->
    @bgPos = '-900px 0'
    super

class @Rock1 extends Rock
  constructor: (data)->
    @bgPos = '0 0'
    super

class @Rock2 extends Rock
  constructor: (data)->
    @bgPos = '-150px 0'
    super

class @Rock3 extends Rock
  constructor: (data)->
    @bgPos = '-300px 0'
    super

class @Rock4 extends Rock
  constructor: (data)->
    @bgPos = '-450px 0'
    super
