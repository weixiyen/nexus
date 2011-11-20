(function() {
  var GRID_H, GRID_W;
  GRID_W = 32;
  GRID_H = 16;
  this.Map = (function() {
    function Map(options) {
      this.$canvas = options.$canvas;
    }
    Map.prototype.reset = function() {
      return this.$canvas.empty();
    };
    Map.prototype.setCollisionGraph = function(graph) {
      return this.graph = $.astar.graph(graph);
    };
    Map.prototype.canWalk = function() {};
    return Map;
  })();
}).call(this);
