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
    Map.prototype.setup = function(graph) {
      this.setDimensions(graph[0].length, graph.length);
      return this.listenToEvents();
    };
    Map.prototype.setDimensions = function(x, y) {
      return this.$canvas.css({
        width: GRID_W * x,
        height: GRID_H * y
      });
    };
    Map.prototype.listenToEvents = function() {
      return this.$canvas.on('click', function(e) {
        var x, y;
        x = Math.round(e.offsetX / GRID_W);
        y = Math.round(e.offsetY / GRID_H);
        return events.moveMe(x, y);
      });
    };
    return Map;
  })();
}).call(this);
