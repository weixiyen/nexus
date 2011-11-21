GRID_W = 32
GRID_H = 16

TILE_W = 302
TILE_H = 176

BUFFER = 2 # for rendering tiles

class @Map

  constructor: (options) ->
    @$canvas = options.$canvas
    @mouseOffsetX = 0
    @mouseOffsetY = 0
    @setClientDimensions()

  reset: ->
    @$canvas.empty()

  setup: (graph) ->
    @setDimensions(graph[0].length, graph.length)
    @listenToEvents()
    @setUpTiles()
    #@renderAllTiles()

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

  setClientDimensions: ->
    @clientX = $window.width()
    @clientY = $window.height()

  render: ->
    left = Math.abs(@left)
    top = Math.abs(@top)
    leftEnd = left + @clientX
    topEnd = top + @clientY

    x1 = Math.floor(left / TILE_W) - BUFFER
    y1 = Math.floor(top / TILE_H) - BUFFER
    x2 = Math.ceil(leftEnd / TILE_W) + BUFFER
    y2 = Math.ceil(topEnd / TILE_H) + BUFFER

    #@removeVisibleTiles(x1, y1, x2, y2)

    for y in [y1...y2]
      for x in [x1...x2]
        continue if !(img=@tiles[y][x])
        continue if @visibleTiles[y] && @visibleTiles[y][x]
        @visibleTiles[y][x] = true
        tile = $('<div/>').css
          background: "no-repeat url("+img+")"
          position: "absolute"
          left: x * TILE_W
          top: y * TILE_H
          width: TILE_W
          height: TILE_H
        tile.appendTo(@$canvas)


    return null

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