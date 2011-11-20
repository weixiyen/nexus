class @Interface

  ABILITIES_BAR_WIDTH = 202

  constructor: (options)->
    @$canvas = options.$canvas
    @$abilities = @$canvas.find('.abilities').first()
    @reload()

  reload: ->
    @$abilities.css
      left: $window.width() / 2 - ABILITIES_BAR_WIDTH / 2
      width: ABILITIES_BAR_WIDTH