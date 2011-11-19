(function() {
  this.Map = (function() {
    function Map(options) {
      this.$canvas = options.$canvas;
    }
    Map.prototype.reset = function() {
      return this.$canvas.empty();
    };
    return Map;
  })();
}).call(this);
