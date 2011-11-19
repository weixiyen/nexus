class @Map

  constructor: (options) ->
    @$canvas = options.$canvas

  reset: ->
    @$canvas.empty()