GRID_W = 32
GRID_H = 16

class @Map

  constructor: (options) ->
    @$canvas = options.$canvas
    @mouseOffsetX = 0
    @mouseOffsetY = 0

  reset: ->
    @$canvas.empty()

  setup: (graph) ->
    @setDimensions(graph[0].length, graph.length)
    @listenToEvents()

  setDimensions: (x, y) ->
    @$canvas.css
      width: GRID_W * x
      height: GRID_H * y

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