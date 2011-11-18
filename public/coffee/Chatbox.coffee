class @Chatbox
  constructor: (data) ->
    @$el = data.el
    @$bg = @$el.find('.ui-chatbox:first')
    @$log = @$el.find('.ui-chatlog:first')
    @setDimensions()
    @bindWindowResize()
  bindWindowResize: ->
    $(window).resize =>
      @setDimensions()
  setDimensions: ->
    @height = settings.partyBox.height
    @width = $(window).width() - settings.partyBox.width * 2 - 12
    @$bg.css
      width: @width
      height: @height
    @$log.css
      width: @width
      height: @height