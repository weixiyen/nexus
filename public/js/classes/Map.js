(function() {
  var BUFFER, GRID_H, GRID_W, TILE_H, TILE_W;
  var __bind = function(fn, me){ return function(){ return fn.apply(me, arguments); }; };
  GRID_W = 32;
  GRID_H = 16;
  TILE_W = 302;
  TILE_H = 176;
  BUFFER = 2;
  this.Map = (function() {
    function Map(options) {
      this.$canvas = options.$canvas;
      this.mouseOffsetX = 0;
      this.mouseOffsetY = 0;
      this.setClientDimensions();
    }
    Map.prototype.reset = function() {
      return this.$canvas.empty();
    };
    Map.prototype.setup = function(graph) {
      this.setDimensions(graph[0].length, graph.length);
      this.listenToEvents();
      return this.setUpTiles();
    };
    Map.prototype.setDimensions = function(x, y) {
      this.width = GRID_W * x;
      this.height = GRID_H * y;
      return this.$canvas.css({
        width: this.width,
        height: this.height
      });
    };
    Map.prototype.listenToEvents = function() {
      this.$canvas.on('click', __bind(function(e) {
        return events.moveMe(this.getMouseX(), this.getMouseY());
      }, this));
      return this.$canvas.on('mousemove', __bind(function(e) {
        this.mouseOffsetX = e.pageX - this.left;
        return this.mouseOffsetY = e.pageY - this.top;
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
    Map.prototype.renderOffset = function(style) {
      this.left = style.left;
      this.top = style.top;
      return this.$canvas.css(style);
    };
    Map.prototype.setUpTiles = function() {
      var path, x, y, _results;
      this.tiles = [];
      _results = [];
      for (y = 0; y < 20; y++) {
        this.tiles[y] = [];
        _results.push((function() {
          var _results2;
          _results2 = [];
          for (x = 0; x < 20; x++) {
            path = ['/public/img/map/', y, '_', x, '.png'].join('');
            _results2.push(this.tiles[y][x] = path);
          }
          return _results2;
        }).call(this));
      }
      return _results;
    };
    Map.prototype.setClientDimensions = function() {
      this.clientX = $window.width();
      return this.clientY = $window.height();
    };
    Map.prototype.render = function() {
      var img, left, leftEnd, tile, top, topEnd, x, x1, x2, y, y1, y2;
      left = Math.abs(this.left);
      top = Math.abs(this.top);
      leftEnd = left + this.clientX;
      topEnd = top + this.clientY;
      x1 = Math.floor(left / TILE_W) - BUFFER;
      y1 = Math.floor(top / TILE_H) - BUFFER;
      x2 = Math.ceil(leftEnd / TILE_W) + BUFFER;
      y2 = Math.ceil(topEnd / TILE_H) + BUFFER;
      for (y = y1; y1 <= y2 ? y < y2 : y > y2; y1 <= y2 ? y++ : y--) {
        for (x = x1; x1 <= x2 ? x < x2 : x > x2; x1 <= x2 ? x++ : x--) {
          if (!(img = this.tiles[y][x])) {
            continue;
          }
          if (this.visibleTiles[y] && this.visibleTiles[y][x]) {
            continue;
          }
          this.visibleTiles[y][x] = true;
          tile = $('<div/>').css({
            background: "no-repeat url(" + img + ")",
            position: "absolute",
            left: x * TILE_W,
            top: y * TILE_H,
            width: TILE_W,
            height: TILE_H
          });
          tile.appendTo(this.$canvas);
        }
      }
      return null;
    };
    Map.prototype.renderAllTiles = function() {
      var htmlArr, img, row, tile, x, y, _len, _ref, _results;
      htmlArr = [];
      _ref = this.tiles;
      _results = [];
      for (y = 0, _len = _ref.length; y < _len; y++) {
        row = _ref[y];
        _results.push((function() {
          var _len2, _results2;
          _results2 = [];
          for (x = 0, _len2 = row.length; x < _len2; x++) {
            img = row[x];
            tile = $('<img/>', {
              src: img,
              css: {
                position: "absolute",
                left: x * TILE_W,
                top: y * TILE_H,
                width: TILE_W,
                height: TILE_H
              }
            });
            _results2.push(tile.appendTo(this.$canvas));
          }
          return _results2;
        }).call(this));
      }
      return _results;
    };
    return Map;
  })();
}).call(this);
