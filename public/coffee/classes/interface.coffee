abilities = [
  {
    attack: 1,
    bgIndex: 1,
    name: "AoE",
    keyCode: 49,
    key: 1,
    mp: 10
  }
  {
    attack: 2,
    bgIndex: 2,
    name: "Slow",
    keyCode: 50,
    key: 2,
    mp: 5
  }
  {
    attack: 3,
    bgIndex: 4,
    name: "Flee",
    keyCode: 51,
    key: 3,
    mp: 15
  }
  {
    attack: 4,
    bgIndex: 5,
    name: "Poison",
    keyCode: 52,
    key: 4,
    mp: 5
  }
  {
    attack: 5,
    bgIndex: 5,
    name: "BOOLEET",
    keyCode: 53,
    key: 5,
    mp: 5
  }
]
###
{
  attack: 5,
  bgIndex: 0,
  name: "Ultimate",
  keyCode: 53,
  key: 5
  mp: 50
}
###
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
    @$ability = {}
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

  reloadUser: ->
    u = game.getUser()
    u.setHp(u.hp)
    u.changeMp(0)
    u.increaseExperience(0)

  showUserDeath: ->
    @setHp(0)
    @setMp(0)
    @setXp(0)
    @setName('Dead')
    @renderAbilityIconsByMp(0)

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
      id = abilityData.attack
      @$ability['abil-'+id] = $('#abil-'+id)

  getAbilityIconFragment: (data)->
    id = data.attack
    bgPos = (-data.bgIndex * 36) + 'px 0'
    key = data.key
    name = data.name
    mp = data.mp
    html = """
    <div class="ability" id="abil-#{id}" title="#{name} - #{mp}MP">
      <div class="key">#{key}</div>
      <div class="frame"></div>
      <div class="icon" style="background-position:#{bgPos}"></div>
    </div>
    """
    return $(html)

  pressAbilityIcon: (id)->
    @$ability['abil-'+id].addClass('on')

  releaseAbilityIcon: (id)->
    @$ability['abil-'+id].removeClass('on')

  renderAbilityIconsByMp: (mp)->
    for ability in abilities
      id = ability.attack
      if ability.mp > mp
        bgPos = (-ability.bgIndex * 36) + 'px -36px'
        @$ability['abil-'+id].addClass('off').find('.icon').first().css
          backgroundPosition: bgPos
      else
        bgPos = (-ability.bgIndex * 36) + 'px 0'
        @$ability['abil-'+id].removeClass('off').find('.icon').first().css
          backgroundPosition: bgPos
