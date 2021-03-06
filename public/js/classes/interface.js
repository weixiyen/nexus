(function() {
  var abilities;
  abilities = [
    {
      attack: 1,
      bgIndex: 1,
      name: "AoE",
      keyCode: 49,
      key: 1,
      mp: 10
    }, {
      attack: 2,
      bgIndex: 2,
      name: "Slow",
      keyCode: 50,
      key: 2,
      mp: 5
    }, {
      attack: 3,
      bgIndex: 4,
      name: "Flee",
      keyCode: 51,
      key: 3,
      mp: 15
    }, {
      attack: 4,
      bgIndex: 5,
      name: "Poison",
      keyCode: 52,
      key: 4,
      mp: 5
    }
  ];
  /*
  {
    attack: 5,
    bgIndex: 0,
    name: "Ultimate",
    keyCode: 53,
    key: 5
    mp: 50
  }
  */
  this.Interface = (function() {
    var ABILITY_BAR_HEIGHT, CHAT_HEIGHT, CHAT_WIDTH, MINIMAP_HEIGHT, MINIMAP_WIDTH, XPBAR_HEIGHT;
    CHAT_WIDTH = 400;
    CHAT_HEIGHT = 150;
    MINIMAP_WIDTH = 200;
    MINIMAP_HEIGHT = 150;
    ABILITY_BAR_HEIGHT = 60;
    XPBAR_HEIGHT = 5;
    function Interface(options) {
      this.$canvas = options.$canvas;
      this.$abilities = this.$canvas.find('.abilities').first();
      this.$chatbox = this.$canvas.find('.chatbox').first();
      this.$minimap = this.$canvas.find('.minimap').first();
      this.$xpbar = this.$canvas.find('.xpbar').first();
      this.$unitframes = this.$canvas.find('.unitframes').first();
      this.$myHp = this.$unitframes.find('.hp').first();
      this.$myMp = this.$unitframes.find('.mp').first();
      this.$myXp = this.$canvas.find('.xp').first();
      this.$myLevel = this.$unitframes.find('.level').first();
      this.$myName = this.$unitframes.find('.name').first();
      this.$ability = {};
      this.addAbilityIcons();
      this.reload();
    }
    Interface.prototype.reload = function() {
      var midBarWidth, winHeight, winWidth;
      winWidth = $window.width();
      winHeight = $window.height();
      midBarWidth = winWidth - (CHAT_WIDTH + MINIMAP_WIDTH) - 20;
      this.$abilities.css({
        left: CHAT_WIDTH + 10,
        width: midBarWidth,
        top: winHeight - ABILITY_BAR_HEIGHT - 5,
        height: ABILITY_BAR_HEIGHT
      });
      this.$chatbox.css({
        left: 5,
        top: winHeight - CHAT_HEIGHT - 5,
        width: CHAT_WIDTH,
        height: CHAT_HEIGHT
      });
      this.$minimap.css({
        left: midBarWidth + CHAT_WIDTH + 15,
        width: MINIMAP_WIDTH,
        height: MINIMAP_HEIGHT,
        top: winHeight - MINIMAP_HEIGHT - 5
      });
      this.$xpbar.css({
        left: CHAT_WIDTH + 10,
        width: midBarWidth,
        height: XPBAR_HEIGHT,
        top: winHeight - XPBAR_HEIGHT - 5
      });
      return this.$canvas.css({
        display: 'block'
      });
    };
    Interface.prototype.reloadUser = function() {
      var u;
      u = game.getUser();
      u.setHp(u.hp);
      u.changeMp(0);
      return u.increaseExperience(0);
    };
    Interface.prototype.showUserDeath = function() {
      this.setHp(0);
      this.setMp(0);
      this.setXp(0);
      this.setName('Dead');
      return this.renderAbilityIconsByMp(0);
    };
    Interface.prototype.setHp = function(percent) {
      return this.$myHp.css({
        width: percent + '%'
      });
    };
    Interface.prototype.setMp = function(percent) {
      return this.$myMp.css({
        width: percent + '%'
      });
    };
    Interface.prototype.setXp = function(percent) {
      return this.$myXp.css({
        width: percent + '%'
      });
    };
    Interface.prototype.setName = function(name) {
      return this.$myName.html(name);
    };
    Interface.prototype.setLevel = function(level) {
      return this.$myLevel.html(level);
    };
    Interface.prototype.addAbilityIcons = function() {
      var abilityData, id, _i, _len, _results;
      _results = [];
      for (_i = 0, _len = abilities.length; _i < _len; _i++) {
        abilityData = abilities[_i];
        this.$abilities.append(this.getAbilityIconFragment(abilityData));
        id = abilityData.attack;
        _results.push(this.$ability['abil-' + id] = $('#abil-' + id));
      }
      return _results;
    };
    Interface.prototype.getAbilityIconFragment = function(data) {
      var bgPos, html, id, key, mp, name;
      id = data.attack;
      bgPos = (-data.bgIndex * 36) + 'px 0';
      key = data.key;
      name = data.name;
      mp = data.mp;
      html = "<div class=\"ability\" id=\"abil-" + id + "\" title=\"" + name + " - " + mp + "MP\">\n  <div class=\"key\">" + key + "</div>\n  <div class=\"frame\"></div>\n  <div class=\"icon\" style=\"background-position:" + bgPos + "\"></div>\n</div>";
      return $(html);
    };
    Interface.prototype.pressAbilityIcon = function(id) {
      return this.$ability['abil-' + id].addClass('on');
    };
    Interface.prototype.releaseAbilityIcon = function(id) {
      return this.$ability['abil-' + id].removeClass('on');
    };
    Interface.prototype.renderAbilityIconsByMp = function(mp) {
      var ability, bgPos, id, _i, _len, _results;
      _results = [];
      for (_i = 0, _len = abilities.length; _i < _len; _i++) {
        ability = abilities[_i];
        id = ability.attack;
        _results.push(ability.mp > mp ? (bgPos = (-ability.bgIndex * 36) + 'px -36px', this.$ability['abil-' + id].addClass('off').find('.icon').first().css({
          backgroundPosition: bgPos
        })) : (bgPos = (-ability.bgIndex * 36) + 'px 0', this.$ability['abil-' + id].removeClass('off').find('.icon').first().css({
          backgroundPosition: bgPos
        })));
      }
      return _results;
    };
    return Interface;
  })();
}).call(this);
