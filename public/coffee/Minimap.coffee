class @Minimap
  constructor: (data) ->
    @$el = data.el
    @$bg = @$el.find('.ui-minimap:first')
    @height = settings.partyBox.height
    @width = settings.partyBox.width
    @create()
  create: ->
    @$bg.css
      width: @width
      height: @height