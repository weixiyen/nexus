class @Sprite
  constructor: ->
  start: (id, opts, callback) ->

    id = 'mm-anim-' + id
    el = opts.el
    queue = opts.queue
    len = queue.length
    skip = opts.skip || 1

    global[ id ] = 0
    $.loop.add id, skip, ->
      el.css
          'background-position': queue[ global[ id ] ]
      if global[ id ] == len
        return global[ id ] = 0
      global[ id ] += 1

    if callback?
      @callback( opts )

  stop: (id) ->
    $.loop.remove 'mm-anim-' + id
  once: (options, callback) ->