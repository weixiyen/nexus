class @Sprite
  constructor: (opts)->
    @id = 'anim:' + opts.id
    @el = opts.el
    @queue = opts.queue
    @skip = opts.skip || 1
    @len = @queue.length
    @counter = 0

  start: ->
    game.addLoopItem @id, @skip, =>
      @el.css
        'background-position': @queue[ @counter ]
      if @counter == @len
        return @counter = 0
      @counter += 1

  stop: ->
    game.removeLoopItem(@id)