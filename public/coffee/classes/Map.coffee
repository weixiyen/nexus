GRID_W = 32
GRID_H = 16

TILE_W = 302
TILE_H = 176

BUFFER = 1 # for rendering tiles
RENDER_INTERVAL = 8

class @Map

  constructor: (options) ->
    @$canvas = options.$canvas
    @mouseOffsetX = 0
    @mouseOffsetY = 0
    @visibleTiles = {}
    @cachedFragments = {}
    @cachedProps = {}

    @setClientDimensions()

  startRenderLoop: ->
    game.addLoopItem('map:render', RENDER_INTERVAL, @render)

  stopRenderLoop: ->
    game.removeLoopItem('map:render')

  reset: ->
    @$canvas.empty()
    @visibleTiles = {}

  setup: (graph) ->
    @graph = graph
    @setDimensions(graph[0].length, graph.length)
    @listenToEvents()
    @setUpTiles()

  renderGraph: ->
    blocks = []
    yMax = @graph.length
    xMax = @graph[0].length
    for y in [0...yMax]
      for x in [0...xMax]
        if @graph[y][x] == 2
          blocks.push(@getCollisionBlock(x, y))
    game.$canvas.find('.collision-block').remove().append.apply(game.$canvas, blocks)
    console.log blocks.length + ' blocks rendered'
    return null

  getCollisionBlock: (x, y)->
    el = $ '<div/>'
      class: 'collision-block'
      css:
        left: x * GRID_W - Math.round(GRID_W / 2)
        top: y * GRID_H - GRID_H
        width: GRID_W
        height: GRID_H
        background: 'rgba(0,0,0,0.7)'
        position: 'absolute'
        zIndex: y * GRID_H + 1000
        color: 'yellow'
        font: '9px Arial'
        textAlign: 'center'
    el.html(x+','+y)

  setDimensions: (x, y) ->
    @width = GRID_W * x
    @height = GRID_H * y

    @$canvas.css
      width: @width
      height: @height

  listenToEvents: ->
    @$canvas.on 'click', (e)=>
      game.moveUser(@getMouseX(), @getMouseY())
      if window.DEBUG == true
        x = Math.round(@mouseOffsetX / GRID_W)
        y = Math.round(@mouseOffsetY / GRID_H)
        map.$canvas.append(@getCollisionBlock(x, y))


    @$canvas.on 'mousemove', (e)=>
      @mouseOffsetX = e.pageX - @left
      @mouseOffsetY = e.pageY - @top

  getMouseX: ->
    return Math.round(@mouseOffsetX / GRID_W)

  getMouseY: ->
    return Math.round(@mouseOffsetY / GRID_H)

  getMouseCoords: ->
    return [@getMouseX(), @getMouseY()]

  renderOffset: (style) ->
    @left = style.left
    @top = style.top
    @$canvas.css(style)

  setUpTiles: ->
    @tiles = []
    for y in [0...20]
      @tiles[y] = []
      for x in [0...20]
        path = ['/public/img/map/', y, '_', x, '.jpg'].join('')
        @tiles[y][x] = path
        txy = 't-'+x+'-'+y
        @cachedFragments[txy] = @getTileFragment(x,y,path)

  associatePropsToTiles: ->
    for id, prop of game.props
      x = Math.floor(prop.left / TILE_W)
      y = Math.floor(prop.top / TILE_H)
      txy = 't-'+x+'-'+y
      if @cachedProps[txy]
        @cachedProps[txy].push(prop)
      else
        @cachedProps[txy] = [prop]

  setClientDimensions: ->
    @clientX = $window.width()
    @clientY = $window.height()

  addToCanvas: ($element)->
    @$canvas.append($element)

  render: =>

    left = Math.abs(@left)
    top = Math.abs(@top)
    leftEnd = left + @clientX
    topEnd = top + @clientY

    x1 = Math.floor(left / TILE_W) - BUFFER
    y1 = Math.floor(top / TILE_H) - BUFFER
    x2 = Math.ceil(leftEnd / TILE_W) + BUFFER
    y2 = Math.ceil(topEnd / TILE_H) + BUFFER

    purgeIds = []
    propPurgeIds = []
    for id, stub of @visibleTiles
      pieces = stub.split('-')
      x = pieces[1]
      y = pieces[2]
      if (x > 0 && y > 0) && ( (x < x1) || (x > x2) || (y < y1) || (y > y2) )
        purgeIds.push('#'+stub)
        delete @visibleTiles[id]
        continue if !(props=@cachedProps[id])
        for prop in props
          propPurgeIds.push('#'+prop.elementId)

    $tilesToRender = []
    $propsToRender = []
    for y in [y1...y2]
      for x in [x1...x2]
        txy = 't-'+x+'-'+y
        continue if !(imgpath=@tiles[y]?[x])
        continue if @visibleTiles[txy]

        @visibleTiles[txy] = txy
        $tilesToRender.push(@cachedFragments[txy])
        continue if !(props=@cachedProps[txy])
        for prop in props
          $propsToRender.push(prop.$el)

    @$canvas.append.apply(@$canvas,$tilesToRender) if $tilesToRender.length > 0
    @$canvas.find(purgeIds.join(',')).remove() if purgeIds.length > 0

    game.$canvas.append.apply(game.$canvas,$propsToRender) if $propsToRender.length > 0
    game.$canvas.find(propPurgeIds.join(',')).remove() if propPurgeIds.length > 0

    return null

  getTileFragment: (x,y,imgpath) ->
    left = x * TILE_W
    top = y * TILE_H
    html = """
      <div id="t-#{x}-#{y}" style="background:url(#{imgpath}) no-repeat;top:#{top}px;left:#{left}px;width:#{TILE_W}px;height:#{TILE_H}px;position:absolute;"></div>
    """
    return $(html)
