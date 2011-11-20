(function() {
  var GRID_H, GRID_W;
  var __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; };
  GRID_W = 32;
  GRID_H = 16;
  this.Map = (function() {
    function Map(options) {
      this.$canvas = options.$canvas;
      this.mouseOffsetX = 0;
      this.mouseOffsetY = 0;
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
      this.$canvas.on('click', __bind(function(e) {
        return events.moveMe(this.getMouseX(), this.getMouseY());
      }, this));
      return this.$canvas.on('mousemove', __bind(function(e) {
        this.mouseOffsetX = e.offsetX;
        return this.mouseOffsetY = e.offsetY;
      }, this));
    };
    Map.prototype.getMouseX = function() {
      return Math.round(this.mouseOffsetX / GRID_W);
    };
    Map.prototype.getMouseY = function() {
      return Math.round(this.mouseOffsetY / GRID_H);
    };
    Map.prototype.getMouseCoords = function() {
      return [this.getMouseX(), this.getMouseY()];
    };
    return Map;
  })();
}).call(this);
