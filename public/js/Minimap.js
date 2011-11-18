(function() {
  this.Minimap = (function() {
    function Minimap(data) {
      this.$el = data.el;
      this.$bg = this.$el.find('.ui-minimap:first');
      this.height = settings.partyBox.height;
      this.width = settings.partyBox.width;
      this.create();
    }
    Minimap.prototype.create = function() {
      return this.$bg.css({
        width: this.width,
        height: this.height
      });
    };
    return Minimap;
  })();
}).call(this);
