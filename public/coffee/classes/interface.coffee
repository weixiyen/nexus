class @Interface

  CHAT_WIDTH = 400
  CHAT_HEIGHT = 150

  MINIMAP_WIDTH = 200
  MINIMAP_HEIGHT = 150

  ABILITY_BAR_HEIGHT = 60

  XPBAR_HEIGHT = 5

  constructor: (options)->
    @$canvas = options.$canvas
    @$abilities = @$canvas.find('.abilities').first()
    @$chatbox = @$canvas.find('.chatbox').first()
    @$minimap = @$canvas.find('.minimap').first()
    @$xpbar = @$canvas.find('.xpbar').first()
    @$unitframes = @$canvas.find('.unitframes').first()
    @$myHp = @$unitframes.find('.hp').first()
    @$myMp = @$unitframes.find('.mp').first()
    @$myXp = @$unitframes.find('.xp').first()
    @reload()

  reload: ->
    winWidth = $window.width()
    winHeight = $window.height()
    midBarWidth = winWidth - (CHAT_WIDTH + MINIMAP_WIDTH) - 20

    @$abilities.css
      left: CHAT_WIDTH + 10
      width: midBarWidth
      top: winHeight - ABILITY_BAR_HEIGHT - 5
      height: ABILITY_BAR_HEIGHT

    @$chatbox.css
      left: 5
      top: winHeight - CHAT_HEIGHT - 5
      width: CHAT_WIDTH
      height: CHAT_HEIGHT

    @$minimap.css
      left: midBarWidth + CHAT_WIDTH + 15
      width: MINIMAP_WIDTH
      height: MINIMAP_HEIGHT
      top: winHeight - MINIMAP_HEIGHT - 5

    @$xpbar.css
      left: CHAT_WIDTH + 10
      width: midBarWidth
      height: XPBAR_HEIGHT
      top: winHeight - XPBAR_HEIGHT - 5

  setHp: (percent)->
    @$myHp.css
      width: percent+'%'

  setMp: (percent)->
    @$myMp.css
      width: percent+'%'

  setXp: (percent)->
    @$myXp.css
      width: percent+'%'