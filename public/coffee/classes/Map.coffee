GRID_W = 32
GRID_H = 16

TILE_W = 302
TILE_H = 176

BUFFER = 1 # for rendering tiles

class @Map

  constructor: (options) ->
    @$canvas = options.$canvas
    @mouseOffsetX = 0
    @mouseOffsetY = 0
    @visibleTiles = {}
    @cachedFragments = {}

    @setClientDimensions()
    @beginRenderLoop()

  beginRenderLoop: ->
    game.addLoopItem 'map:render', 10, @render

  reset: ->
    @$canvas.empty()

  setup: (graph) ->
    @setDimensions(graph[0].length, graph.length)
    @listenToEvents()
    @setUpTiles()

  setDimensions: (x, y) ->
    @width = GRID_W * x
    @height = GRID_H * y

    @$canvas.css
      width: @width
      height: @height

  listenToEvents: ->
    @$canvas.on 'click', (e)=>
      events.moveMe(@getMouseX(), @getMouseY())

    @$canvas.on 'mousemove', (e)=>
      @mouseOffsetX = e.pageX - @left
      @mouseOffsetY = e.pageY - @top

  getMouseX: ->
    return Math.round(@mouseOffsetX / GRID_W)

  getMouseY: ->
    return Math.round(@mouseOffsetY / GRID_H)

  getMouseCoords: ->
    return [@getMouseX(), @getMouseY()]

  renderOffset: (style) ->
    @left = style.left
    @top = style.top
    @$canvas.css(style)

  setUpTiles: ->
    @tiles = []
    for y in [0...20]
      @tiles[y] = []
      for x in [0...20]
        path = ['/public/img/map/', y, '_', x, '.png'].join('')
        @tiles[y][x] = path
        txy = 't-'+x+'-'+y
        @cachedFragments[txy] = @getTileFragment(x,y,path)

  setClientDimensions: ->
    @clientX = $window.width()
    @clientY = $window.height()

  render: =>
    left = Math.abs(@left)
    top = Math.abs(@top)
    leftEnd = left + @clientX
    topEnd = top + @clientY

    x1 = Math.floor(left / TILE_W) - BUFFER
    y1 = Math.floor(top / TILE_H) - BUFFER
    x2 = Math.ceil(leftEnd / TILE_W) + BUFFER
    y2 = Math.ceil(topEnd / TILE_H) + BUFFER

    purgeIds = []
    for id, stub of @visibleTiles
      pieces = stub.split('-')
      x = pieces[1]
      y = pieces[2]
      if (x < x1) || (x > x2) || (y < y1) || (y > y2)
        purgeIds.push('#'+stub)
        delete @visibleTiles[id]

    for y in [y1...y2]
      for x in [x1...x2]
        txy = 't-'+x+'-'+y
        continue if !(imgpath=@tiles[y]?[x])
        continue if @visibleTiles[txy]

        @visibleTiles[txy] = txy
        @$canvas.append( @cachedFragments[txy] )

    @$canvas.find(purgeIds.join(',')).remove()
    return null

  getTileFragment: (x,y,imgpath) ->
    left = x * TILE_W
    top = y * TILE_H
    html = """
      <div id="t-#{x}-#{y}" style="background:url(#{imgpath}) no-repeat;top:#{top}px;left:#{left}px;width:#{TILE_W}px;height:#{TILE_H}px;position:absolute;"></div>
    """
    return $(html)

  renderAllTiles: ->
    htmlArr = []
    for row, y in @tiles
      for img, x in row
        tile = $ '<img/>',
          src: img
          css:
            position: "absolute"
            left: x * TILE_W
            top: y * TILE_H
            width: TILE_W
            height: TILE_H
        tile.appendTo(@$canvas)