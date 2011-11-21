(function() {
  var abilities;
  abilities = [
    {
      attack: 1,
      background: 108,
      name: "Attack",
      keyCode: 1
    }
  ];
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
      var abilityData, _i, _len, _results;
      _results = [];
      for (_i = 0, _len = abilities.length; _i < _len; _i++) {
        abilityData = abilities[_i];
        _results.push(console.log(abilityData));
      }
      return _results;
    };
    Interface.prototype.getAbilityIconFragment = function(data) {
      var html;
      console.log(data);
      html = "<div>lol</div>";
      return this(html);
    };
    return Interface;
  })();
}).call(this);
