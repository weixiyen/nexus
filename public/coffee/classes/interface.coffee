abilities = [
  {
    attack: 1,
    bgIndex: 1,
    name: "AoE",
    keyCode: 49,
    key: 1
  }
  {
    attack: 2,
    bgIndex: 2,
    name: "Slow",
    keyCode: 50,
    key: 2
  }
  {
    attack: 3,
    bgIndex: 4,
    name: "Flee",
    keyCode: 51,
    key: 3
  }
  {
    attack: 4,
    bgIndex: 5,
    name: "Slow",
    keyCode: 52,
    key: 4
  }
  {
    attack: 5,
    bgIndex: 0,
    name: "Slow",
    keyCode: 53,
    key: 5
  }
]
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
    @$myXp = @$canvas.find('.xp').first()
    @$myLevel = @$unitframes.find('.level').first()
    @$myName = @$unitframes.find('.name').first()
    @addAbilityIcons()
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

    @$canvas.css
      display: 'block'

  setHp: (percent)->
    @$myHp.css
      width: percent+'%'

  setMp: (percent)->
    @$myMp.css
      width: percent+'%'

  setXp: (percent)->
    @$myXp.css
      width: percent+'%'

  setName: (name)->
    @$myName.html(name)

  setLevel: (level)->
    @$myLevel.html(level)

  addAbilityIcons: ->
    for abilityData in abilities
      @$abilities.append(@getAbilityIconFragment(abilityData))

  getAbilityIconFragment: (data)->
    bgPos = (-data.bgIndex * 36) + 'px ' + 0
    key = data.key
    html = """
    <div class="ability">
      <div class="key">#{key}</div>
      <div class="frame"></div>
      <div class="icon" style="background-position:#{bgPos}"></div>
    </div>
    """
    return $(html)