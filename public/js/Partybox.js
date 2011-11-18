(function() {
  this.Partybox = (function() {
    function Partybox(data) {
      this.$el = data.el;
      this.$bg = this.$el.find('.ui-partybox:first');
      this.height = settings.partyBox.height;
      this.width = settings.partyBox.width;
      this.create();
    }
    Partybox.prototype.create = function() {
      return this.$bg.css({
        width: this.width,
        height: this.height
      });
    };
    return Partybox;
  })();
}).call(this);
