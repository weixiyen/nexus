class @Sprite
  constructor: (opts)->
    @id = 'anim:' + opts.id
    @el = opts.el
    @index0 = opts.index0 or 1
    @counter = @index0

  start: (queue, skip)->
    len = queue.length
    game.addLoopItem @id, skip, =>
      @el.css
        'background-position': queue[ @counter ]
      @counter += 1
      if @counter == len
        @counter = @index0

  set: (position)->
    @el.css
      'background-position': position

  stop: ->
    game.removeLoopItem(@id)