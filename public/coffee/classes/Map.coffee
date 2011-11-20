GRID_W = 32
GRID_H = 16

class @Map

  constructor: (options) ->
    @$canvas = options.$canvas

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
    @$canvas.on 'click', (e)->
      x = Math.round(e.offsetX / GRID_W)
      y = Math.round(e.offsetY / GRID_H)
      events.moveMe(x, y)