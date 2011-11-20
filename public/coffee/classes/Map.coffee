GRID_W = 32
GRID_H = 16

class @Map

  constructor: (options) ->
    @$canvas = options.$canvas

  reset: ->
    @$canvas.empty()

  setCollisionGraph: (graph) ->
    @graph = $.astar.graph graph

  canWalk: ->