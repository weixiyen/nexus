(function() {
  this.Interface = (function() {
    var ABILITIES_BAR_WIDTH;
    ABILITIES_BAR_WIDTH = 202;
    function Interface(options) {
      this.$canvas = options.$canvas;
      this.$abilities = this.$canvas.find('.abilities').first();
      this.reload();
    }
    Interface.prototype.reload = function() {
      return this.$abilities.css({
        left: $window.width() / 2 - ABILITIES_BAR_WIDTH / 2,
        width: ABILITIES_BAR_WIDTH
      });
    };
    return Interface;
  })();
}).call(this);
