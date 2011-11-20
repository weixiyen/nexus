class @Sprite
  constructor: (opts)->
    @id = 'anim:' + opts.id
    @el = opts.el
    @counter = 0

  start: (queue, skip)->
    len = queue.length
    game.addLoopItem @id, skip, =>
      @el.css
        'background-position': queue[ @counter ]
      @counter += 1
      if @counter == len
        @counter = 0

  stop: ->
    game.removeLoopItem(@id)