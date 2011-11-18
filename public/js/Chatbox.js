(function() {
  var __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; };
  this.Chatbox = (function() {
    function Chatbox(data) {
      this.$el = data.el;
      this.$bg = this.$el.find('.ui-chatbox:first');
      this.$log = this.$el.find('.ui-chatlog:first');
      this.setDimensions();
      this.bindWindowResize();
    }
    Chatbox.prototype.bindWindowResize = function() {
      return $(window).resize(__bind(function() {
        return this.setDimensions();
      }, this));
    };
    Chatbox.prototype.setDimensions = function() {
      this.height = settings.partyBox.height;
      this.width = $(window).width() - settings.partyBox.width * 2 - 12;
      this.$bg.css({
        width: this.width,
        height: this.height
      });
      return this.$log.css({
        width: this.width,
        height: this.height
      });
    };
    return Chatbox;
  })();
}).call(this);
